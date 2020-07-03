import re

from cleo.testers import ApplicationTester

from entrypoints import EntryPoint
from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin


class FooCommand(Command):
    name = "foo"

    description = "Foo Command"

    def handle(self):
        self.line("foo called")

        return 0


class AddCommandPlugin(ApplicationPlugin):
    def activate(self, application):
        application.add(FooCommand())


def test_application_with_plugins(mocker):
    mocker.patch(
        "entrypoints.get_group_all",
        return_value=[
            EntryPoint(
                "my-plugin", "tests.console.test_application", "AddCommandPlugin"
            )
        ],
    )

    app = Application()
    app.config.set_terminate_after_run(False)

    tester = ApplicationTester(app)
    tester.execute("")

    print(tester.io.fetch_output())
    assert re.search(r"foo\s+Foo Command", tester.io.fetch_output()) is not None
    assert 0 == tester.status_code


def test_application_execute_plugin_command(mocker):
    mocker.patch(
        "entrypoints.get_group_all",
        return_value=[
            EntryPoint(
                "my-plugin", "tests.console.test_application", "AddCommandPlugin"
            )
        ],
    )

    app = Application()
    app.config.set_terminate_after_run(False)

    tester = ApplicationTester(app)
    tester.execute("foo")

    assert "foo called\n" == tester.io.fetch_output()
    assert 0 == tester.status_code
