from catlauncher.launcher import LaunchConfig, build_java_command, validate_config


def test_validate_config_requires_jar():
    config = LaunchConfig(
        username="Cat",
        java_path="/usr/bin/java",
        game_dir="/tmp/minecraft",
        minecraft_jar="",
    )

    errors = validate_config(config)

    assert "minecraft_jar" in errors


def test_build_java_command_contains_required_arguments():
    config = LaunchConfig(
        username="Cat",
        java_path="/usr/bin/java",
        game_dir="/tmp/minecraft",
        minecraft_jar="/tmp/client.jar",
        memory_mb=2048,
        width=1280,
        height=720,
    )

    command = build_java_command(config)

    assert command[0] == "/usr/bin/java"
    assert "-Xmx2048M" in command
    assert "-Xms512M" in command
    assert "/tmp/client.jar" in command
    assert "--width" in command
    assert "1280" in command
