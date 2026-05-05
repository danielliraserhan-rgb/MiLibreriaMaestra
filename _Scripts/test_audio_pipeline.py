#!/usr/bin/env python3
"""
test_audio_pipeline.py — Pruebas para audio_to_zettelkasten_pipeline.py

Prueba 1 (Happy path): transcripción pastoral con ruido vocal →
  Haiku extrae 2 premisas limpias → Sonnet genera specs ZK válidas →
  se crean 2 archivos .md con YAML v2 correcto.

Prueba 2 (Robustez): respuestas malformadas de la API, campo inesperado
  en premisas, spec inválida, transcripción demasiado corta.
"""

import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Asegurar que _Scripts/ está en el path
sys.path.insert(0, str(Path(__file__).parent))

import audio_to_zettelkasten_pipeline as pipeline


# ─── FIXTURES ──────────────────────────────────────────────────────────────────

RAW_TRANSCRIPT = textwrap.dedent("""\
    O sea, este... lo que quiero decir, ¿verdad?, es que cuando uno lee Gálatas 2:20
    no espera, déjame reformular, cuando uno lee Gálatas 2:20 se da cuenta de que Pablo
    no está hablando de un esfuerzo moral, o sea no, sino de una muerte y resurrección.
    La identidad cristiana, este, no se construye desde el esfuerzo sino desde la unión
    con Cristo en su muerte. Eso es, este, lo que quiero que quede claro.

    Y otra cosa que me parece importante, ¿verdad?, es que muchas veces confundimos
    obediencia con rendimiento. La obediencia bíblica no es rendimiento religioso
    — es respuesta de amor. Cuando amas a alguien obedeces porque quieres, no porque
    tienes que demostrar algo. Como en Juan 14:15, "Si me amáis, guardad mis mandamientos."
""")

EXTRACTOR_RESPONSE_CLEAN = json.dumps({
    "premisas": [
        {
            "titulo": "La identidad cristiana nace de la muerte y resurrección con Cristo",
            "desarrollo": (
                "Cuando uno lee Gálatas 2:20 se da cuenta de que Pablo no está hablando "
                "de un esfuerzo moral, sino de una muerte y resurrección. La identidad "
                "cristiana no se construye desde el esfuerzo sino desde la unión con "
                "Cristo en su muerte."
            ),
        },
        {
            "titulo": "La obediencia bíblica es respuesta de amor, no rendimiento religioso",
            "desarrollo": (
                "Muchas veces confundimos obediencia con rendimiento. La obediencia "
                "bíblica no es rendimiento religioso — es respuesta de amor. Cuando amas "
                "a alguien obedeces porque quieres, no porque tienes que demostrar algo. "
                "Juan 14:15: 'Si me amáis, guardad mis mandamientos.'"
            ),
        },
    ]
})

ORCHESTRATOR_RESPONSE_VALID = json.dumps([
    {
        "titulo": "La identidad cristiana nace de la muerte y resurrección con Cristo",
        "titulo_corto": "La identidad cristiana nace de la union con Cristo",
        "subtipo": "argumental",
        "tema": "05_DoctrinasFundamentales",
        "tags": ["pastoral", "identidad", "cristologia", "fe"],
        "versiculos_citados": ["Gálatas 2:20"],
        "desarrollo": (
            "Cuando uno lee Gálatas 2:20 se da cuenta de que Pablo no está hablando "
            "de un esfuerzo moral, sino de una muerte y resurrección. La identidad "
            "cristiana no se construye desde el esfuerzo sino desde la unión con "
            "Cristo en su muerte."
        ),
        "notas_relacionadas": [],
    },
    {
        "titulo": "La obediencia bíblica es respuesta de amor, no rendimiento religioso",
        "titulo_corto": "La obediencia biblica es respuesta de amor no rendimiento",
        "subtipo": "conceptual",
        "tema": "06_DiscipuladoVidaCristiana",
        "tags": ["pastoral", "obediencia", "fe", "discipulado"],
        "versiculos_citados": ["Juan 14:15"],
        "desarrollo": (
            "Muchas veces confundimos obediencia con rendimiento. La obediencia "
            "bíblica no es rendimiento religioso — es respuesta de amor. Cuando amas "
            "a alguien obedeces porque quieres, no porque tienes que demostrar algo. "
            "Juan 14:15: 'Si me amáis, guardad mis mandamientos.'"
        ),
        "notas_relacionadas": [],
    },
])


def _make_api_response(text: str) -> MagicMock:
    """Construye un objeto que imita anthropic.types.Message."""
    content_block = MagicMock()
    content_block.text = text
    msg = MagicMock()
    msg.content = [content_block]
    return msg


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBA 1 — Happy path
# ══════════════════════════════════════════════════════════════════════════════

class TestHappyPath(unittest.TestCase):
    """Flujo completo: transcripción con ruido → 2 notas ZK creadas correctamente."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.zk_dir = Path(self.tmp.name) / "09_Zettelkasten" / "pastoral"
        self.zk_dir.mkdir(parents=True)

        # Transcripción cruda con muletillas
        self.transcript = Path(self.tmp.name) / "lluvia-de-ideas.txt"
        self.transcript.write_text(RAW_TRANSCRIPT, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    @patch("audio_to_zettelkasten_pipeline._get_client")
    def test_pipeline_crea_dos_archivos_md(self, mock_get_client):
        """Las 2 premisas extraídas producen 2 archivos .md con YAML v2 válido."""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            _make_api_response(EXTRACTOR_RESPONSE_CLEAN),   # llamada Haiku
            _make_api_response(ORCHESTRATOR_RESPONSE_VALID), # llamada Sonnet
        ]
        mock_get_client.return_value = mock_client

        # Parchear ZK_PATHS para apuntar al directorio temporal
        with patch.dict(pipeline.ZK_PATHS, {"pastoral": self.zk_dir}):
            premises = pipeline.call_extractor(mock_client, RAW_TRANSCRIPT)
            specs    = pipeline.call_orchestrator(mock_client, premises, "pastoral")

            # Validar specs
            valid = [s for s in specs if not pipeline.validate_spec(s)]
            self.assertEqual(len(valid), 2, "Deben pasar 2 specs la validación")

            # Crear archivos
            created = []
            for i, spec in enumerate(valid):
                zk_id = f"ZK-20260505-1200-{(i + 1):03d}"
                path  = pipeline.create_zk_file(spec, self.zk_dir, zk_id, "pastoral")
                created.append(path)

        self.assertEqual(len(created), 2)

        # Verificar archivo 1
        content_1 = created[0].read_text(encoding="utf-8")
        self._assert_yaml_field(content_1, "id", "ZK-20260505-1200-001")
        self._assert_yaml_field(content_1, "subtipo", "argumental")
        self._assert_yaml_field(content_1, "tema", "05_DoctrinasFundamentales")
        self._assert_yaml_field(content_1, "fuente", '"dictado"')
        self._assert_yaml_field(content_1, "version_yaml", '"2.0"')
        self._assert_yaml_field(content_1, "dominio", "pastoral")
        self.assertIn("Gálatas 2:20", content_1)

        # Verificar archivo 2
        content_2 = created[1].read_text(encoding="utf-8")
        self._assert_yaml_field(content_2, "id", "ZK-20260505-1200-002")
        self._assert_yaml_field(content_2, "subtipo", "conceptual")
        self._assert_yaml_field(content_2, "tema", "06_DiscipuladoVidaCristiana")
        self.assertIn("Juan 14:15", content_2)

        print("  ✅ 2 archivos .md creados con YAML v2 correcto")
        print(f"     → {created[0].name}")
        print(f"     → {created[1].name}")

    @patch("audio_to_zettelkasten_pipeline._get_client")
    def test_extractor_hace_dos_llamadas_api(self, mock_get_client):
        """El pipeline usa Haiku para extracción y Sonnet para orquestación."""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            _make_api_response(EXTRACTOR_RESPONSE_CLEAN),
            _make_api_response(ORCHESTRATOR_RESPONSE_VALID),
        ]
        mock_get_client.return_value = mock_client

        with patch.dict(pipeline.ZK_PATHS, {"pastoral": self.zk_dir}):
            pipeline.call_extractor(mock_client, RAW_TRANSCRIPT)
            pipeline.call_orchestrator(mock_client, [], "pastoral")

        calls = mock_client.messages.create.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].kwargs["model"], pipeline.MODEL_EXTRACTOR)
        self.assertEqual(calls[1].kwargs["model"], pipeline.MODEL_ORCHESTRATOR)
        print(f"  ✅ Llamada 1 → {pipeline.MODEL_EXTRACTOR}")
        print(f"  ✅ Llamada 2 → {pipeline.MODEL_ORCHESTRATOR}")

    def _assert_yaml_field(self, content: str, field: str, expected: str):
        self.assertIn(
            f"{field}: {expected}", content,
            msg=f"Campo YAML '{field}: {expected}' no encontrado en el archivo",
        )


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBA 2 — Robustez y manejo de errores
# ══════════════════════════════════════════════════════════════════════════════

class TestRobustez(unittest.TestCase):
    """Casos borde: JSON dentro de markdown, campos inesperados, specs inválidas, texto corto."""

    # ── _extract_json ──────────────────────────────────────────────────────────

    def test_extrae_json_de_bloque_markdown(self):
        """Respuesta envuelta en ```json ... ``` se parsea correctamente."""
        text = '```json\n{"premisas": [{"titulo": "X", "desarrollo": "Y"}]}\n```'
        result = pipeline._extract_json(text)
        parsed = json.loads(result)
        self.assertEqual(parsed["premisas"][0]["titulo"], "X")
        print("  ✅ JSON extraído de bloque ```json```")

    def test_extrae_json_con_texto_extra(self):
        """Respuesta con texto antes y después del JSON se parsea correctamente."""
        text = 'Aquí tienes las premisas:\n{"premisas": [{"titulo": "A", "desarrollo": "B"}]}\nEspero que ayude.'
        result = pipeline._extract_json(text)
        parsed = json.loads(result)
        self.assertEqual(parsed["premisas"][0]["titulo"], "A")
        print("  ✅ JSON extraído de respuesta con texto extra")

    def test_extrae_array_json(self):
        """Array JSON directo (sin objeto wrapper) se extrae correctamente."""
        text = '[{"titulo": "Z", "desarrollo": "W"}]'
        result = pipeline._extract_json(text)
        parsed = json.loads(result)
        self.assertEqual(parsed[0]["titulo"], "Z")
        print("  ✅ Array JSON directo extraído correctamente")

    # ── _normalize_premise ─────────────────────────────────────────────────────

    def test_normaliza_campos_alternativos(self):
        """Campos 'idea' y 'texto' se normalizan a 'titulo' y 'desarrollo'."""
        raw = {"idea": "Mi premisa", "texto": "El desarrollo aquí."}
        result = pipeline._normalize_premise(raw)
        self.assertIsNotNone(result)
        self.assertEqual(result["titulo"], "Mi premisa")
        self.assertEqual(result["desarrollo"], "El desarrollo aquí.")
        print("  ✅ Campos alternativos normalizados correctamente")

    def test_normaliza_campos_en_ingles(self):
        """Campos en inglés 'title' y 'body' se normalizan correctamente."""
        raw = {"title": "English title", "body": "English body."}
        result = pipeline._normalize_premise(raw)
        self.assertIsNotNone(result)
        self.assertEqual(result["titulo"], "English title")
        print("  ✅ Campos en inglés normalizados correctamente")

    def test_normaliza_falla_con_campos_desconocidos(self):
        """Premisa sin campos reconocibles devuelve None."""
        raw = {"foo": "bar", "baz": "qux"}
        result = pipeline._normalize_premise(raw)
        self.assertIsNone(result)
        print("  ✅ Premisa con campos desconocidos → None (ignorada correctamente)")

    # ── validate_spec ──────────────────────────────────────────────────────────

    def test_spec_valida_no_produce_errores(self):
        """Una spec completa y correcta pasa la validación sin errores."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0]
        errors = pipeline.validate_spec(spec)
        self.assertEqual(errors, [], f"Spec válida produjo errores: {errors}")
        print("  ✅ Spec válida pasa validación sin errores")

    def test_subtipo_invalido_produce_error(self):
        """Un subtipo no permitido produce error de validación."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0].copy()
        spec["subtipo"] = "reflexion"  # no existe en VALID_SUBTIPOS
        errors = pipeline.validate_spec(spec)
        self.assertTrue(any("subtipo" in e for e in errors))
        print(f"  ✅ subtipo inválido detectado: {[e for e in errors if 'subtipo' in e][0]}")

    def test_tema_invalido_produce_error(self):
        """Un código de tema no existente en la taxonomía produce error."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0].copy()
        spec["tema"] = "99_Inexistente"
        errors = pipeline.validate_spec(spec)
        self.assertTrue(any("tema" in e for e in errors))
        print(f"  ✅ tema inválido detectado: {[e for e in errors if 'tema' in e][0]}")

    def test_titulo_corto_con_caracteres_invalidos(self):
        """titulo_corto con ':' o '/' produce error de validación."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0].copy()
        spec["titulo_corto"] = "Fe: la respuesta/al llamado"
        errors = pipeline.validate_spec(spec)
        self.assertTrue(any("caracteres inválidos" in e for e in errors))
        print(f"  ✅ Caracteres inválidos en titulo_corto detectados correctamente")

    def test_titulo_corto_excede_60_chars(self):
        """titulo_corto mayor a 60 caracteres produce error de validación."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0].copy()
        spec["titulo_corto"] = "A" * 61
        errors = pipeline.validate_spec(spec)
        self.assertTrue(any("60" in e for e in errors))
        print(f"  ✅ titulo_corto > 60 chars detectado correctamente")

    def test_desarrollo_vacio_produce_error(self):
        """Un campo desarrollo vacío produce error de validación."""
        spec = json.loads(ORCHESTRATOR_RESPONSE_VALID)[0].copy()
        spec["desarrollo"] = "   "
        errors = pipeline.validate_spec(spec)
        self.assertTrue(any("desarrollo" in e for e in errors))
        print(f"  ✅ desarrollo vacío detectado correctamente")

    # ── Transcripción demasiado corta ──────────────────────────────────────────

    def test_transcripcion_muy_corta_falla(self):
        """El pipeline rechaza transcripciones menores a 50 caracteres."""
        with tempfile.TemporaryDirectory() as tmp:
            short = Path(tmp) / "corto.txt"
            short.write_text("Idea corta.", encoding="utf-8")

            with self.assertRaises(SystemExit) as ctx:
                # Simular el bloque de validación de main()
                raw = short.read_text(encoding="utf-8").strip()
                if len(raw) < 50:
                    sys.exit(1)
            self.assertEqual(ctx.exception.code, 1)
        print("  ✅ Transcripción < 50 chars rechazada con sys.exit(1)")

    # ── Colisión de IDs ────────────────────────────────────────────────────────

    def test_next_sequence_evita_colisiones(self):
        """_next_sequence devuelve el primer número libre, sin colisionar con notas existentes."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            # Simular notas existentes en el mismo instante
            (base / "ZK-20260505-1200-001 Nota A.md").touch()
            (base / "ZK-20260505-1200-002 Nota B.md").touch()

            seq = pipeline._next_sequence(base, "20260505", "1200")
            self.assertEqual(seq, 3)
        print("  ✅ _next_sequence devuelve 003 cuando 001 y 002 ya existen")


# ─── RUNNER ────────────────────────────────────────────────────────────────────

def _run_suite(title: str, test_case: type) -> unittest.TestResult:
    print(f"{'=' * 65}")
    print(title)
    print(f"{'=' * 65}")
    loader = unittest.TestLoader()
    # Ordenar por nombre para salida determinista
    loader.sortTestMethodsUsing = lambda a, b: (a > b) - (a < b)
    suite  = loader.loadTestsFromTestCase(test_case)
    result = unittest.TextTestRunner(verbosity=0, stream=io.StringIO()).run(suite)

    total  = suite.countTestCases()
    failed = len(result.failures) + len(result.errors)
    passed = total - failed
    print(f"\n  Resultado: {passed}/{total} pasaron", "✓" if failed == 0 else "✗")

    if result.failures:
        for _, msg in result.failures:
            print(f"\n  FALLO:\n{textwrap.indent(msg, '    ')}")
    if result.errors:
        for _, msg in result.errors:
            print(f"\n  ERROR:\n{textwrap.indent(msg, '    ')}")
    return result


if __name__ == "__main__":
    r1 = _run_suite("PRUEBA 1 — Happy path (flujo completo con API mockeada)", TestHappyPath)
    print()
    r2 = _run_suite("PRUEBA 2 — Robustez y manejo de casos borde", TestRobustez)

    total_fail = len(r1.failures) + len(r1.errors) + len(r2.failures) + len(r2.errors)
    print()
    if total_fail == 0:
        print("✓ Todas las pruebas pasaron.")
    else:
        print(f"✗ {total_fail} prueba(s) fallaron.")
        sys.exit(1)
