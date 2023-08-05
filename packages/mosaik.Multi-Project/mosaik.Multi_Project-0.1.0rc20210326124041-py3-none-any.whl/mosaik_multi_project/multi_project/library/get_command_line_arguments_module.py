def get_command_line_arguments(
    *,
    operations,
    parallel,
    projects,
    target,
):
    arguments = []
    arguments += [
        '--parallel', parallel,
    ]
    arguments += [
        '--target', target,
    ]
    for operation in operations:
        arguments += [
            '--operation', operation,
        ]
    for project in projects:
        arguments += [
            '--project', project,
        ]
    return arguments
