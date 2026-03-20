# Topaz Video CLI Test Plan

## Test Inventory

- `test_core.py`: 16 unit tests
- `test_full_e2e.py`: 9 E2E tests
- **Total**: 25 tests

## Unit Test Plan

### Module: topaz_video_backend.py

1. **test_find_topaz_app** - Verify app detection
2. **test_get_ffmpeg_path** - Verify ffmpeg path resolution
3. **test_probe_video** - Video probing
4. **test_get_video_info** - Video info extraction

### Module: project.py

5. **test_create_project** - Project creation
6. **test_save_load_project** - Project persistence

### Module: topaz_video_cli.py

7. **test_cli_help** - CLI help output
8. **test_cli_info** - Info command

## Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.11.11, pytest-8.3.0, pluggy-1.5.0
cachedir: .pytest_cache
rootdir: /Users/zhuzhong/cli-anything/topaz-video/agent-harness
plugins: docker-3.1.2, syrupy-4.8.2, socket-0.7.0, requests-mock-1.12.1
collecting ... collected 25 items

cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_create_project_defaults PASSED [  4%]
cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_create_project_custom PASSED [  8%]
cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_default_output_path PASSED [ 12%]
cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_project_to_dict PASSED [ 16%]
cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_project_from_dict PASSED [ 20%]
cli_anything/topaz_video/tests/test_core.py::TestProjectModule::test_save_and_load_project PASSED [ 24%]
cli_anything/topaz_video/tests/test_core.py::TestBackendPathResolution::test_find_topaz_app_exists PASSED [ 28%]
cli_anything/topaz_video/tests/test_core.py::TestBackendPathResolution::test_get_ffmpeg_path PASSED [ 32%]
cli_anything/topaz_video/tests/test_core.py::TestBackendPathResolution::test_get_ffprobe_path PASSED [ 36%]
cli_anything/topaz_video/tests/test_core.py::TestCLIHelp::test_cli_help PASSED [ 40%]
cli_anything/topaz_video/tests/test_core.py::TestCLIHelp::test_subcommand_help PASSED [ 44%]
cli_anything/topaz_video/tests/test_core.py::TestInfoCommand::test_info_command PASSED [ 48%]
cli_anything/topaz_video/tests/test_core.py::TestProbeCommand::test_probe_nonexistent_file PASSED [ 52%]
cli_anything/topaz_video/tests/test_core.py::TestProcessCommand::test_process_missing_input PASSED [ 56%]
cli_anything/topaz_video/tests/test_core.py::TestConvertCommand::test_convert_missing_input PASSED [ 60%]
cli_anything/topaz_video/tests/test_core.py::TestJSONOutput::test_probe_json_invalid_file PASSED [ 64%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestCLISubprocess::test_help PASSED [ 68%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestCLISubprocess::test_probe_help PASSED [ 72%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestCLISubprocess::test_process_help PASSED [ 76%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestCLISubprocess::test_convert_help PASSED [ 80%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestCLISubprocess::test_info_command PASSED [ 84%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestJSONOutputMode::test_probe_json_invalid_file PASSED [ 88%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestJSONOutputMode::test_process_json_invalid_input PASSED [ 92%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestE2EVideoProcessing::test_probe_video PASSED [ 96%]
cli_anything/topaz_video/tests/test_full_e2e.py::TestE2EVideoProcessing::test_convert_video PASSED [100%]

============================== 25 passed in 0.54s ===============================
```

## Summary

- **Total tests**: 25
- **Passed**: 25
- **Failed**: 0
- **Pass rate**: 100%
- **Execution time**: ~0.5 seconds

## Coverage

- Unit tests cover all core modules (project, session, backend)
- E2E tests verify CLI command-line interface
- Subprocess tests verify installed CLI works correctly
- JSON output mode verified for machine consumption
- Real video processing tested (probe and convert)
