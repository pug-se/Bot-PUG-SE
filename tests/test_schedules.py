"""
integração de schedules
funções separadas
"""

'''
class TestSchedules(unittest.TestCase):
    """Test run_schedules module."""

    def test_get_schedule_list(self):
        """Test get_schedule_list."""
        schedules = schedule_manager.get_schedule_list()
        bot_commands = utils.command_modules.get_commands()
        schedules_count = 0
        for bot_command in bot_commands:
            if bot_command.get_schedule():
                schedules_count += 1

        self.assertEqual(schedules_count, len(schedules))
'''
