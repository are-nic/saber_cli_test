import pytest
from app import BuildSystem


@pytest.fixture
def build_system():
    return BuildSystem('yaml_files/tasks.yaml', 'yaml_files/builds.yaml')


def test_list_builds_or_tasks(build_system, capsys):
    build_system.list_builds_or_tasks('builds')
    captured = capsys.readouterr()
    assert "List of available builds:" in captured.out
    assert "* approach_important" in captured.out
    assert "* audience_stand" in captured.out

    build_system.list_builds_or_tasks('tasks')
    captured = capsys.readouterr()
    assert "List of available tasks:" in captured.out
    assert "* create_green_cyclops" in captured.out
    assert "* design_silver_cyclops" in captured.out


def test_get_task(build_system, capsys):
    build_system.get_task('design_olive_cyclops')
    captured = capsys.readouterr()
    assert "Task info:" in captured.out
    assert "* name: design_olive_cyclops" in captured.out
    assert "* dependencies: coloring_green_cyclops, create_green_cyclops, design_teal_cyclops" in captured.out

    build_system.get_task('nonexistent_task')
    captured = capsys.readouterr()
    assert "The task 'nonexistent_task' isn't exists." in captured.out


def test_get_build(build_system, capsys):
    build_system.get_build('audience_stand')
    captured = capsys.readouterr()
    assert "Build info:" in captured.out
    assert "* name: audience_stand" in captured.out
    assert "* tasks: enable_fuchsia_fairies, read_blue_witches, upgrade_olive_gnomes" in captured.out

    build_system.get_build('nonexistent_build')
    captured = capsys.readouterr()
    assert "The build 'nonexistent_build' isn't exists." in captured.out