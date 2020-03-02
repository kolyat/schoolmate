# Schoolmate - school management system
# Copyright (C) 2018-2020  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.utils.translation import gettext_lazy as _
import pytest

from testutils import settings, webutils
from . import data_test_api_diary


class TestDiary(webutils.SchoolmateClient):
    """Test diary web interface
    """
    DATEPICKER = {'selector': '//div[@view_id="current_date"]', 'by': By.XPATH}
    SUBJECT_SELECT = {'selector': '//div[@class="webix_dt_editor"]/select',
                      'by': By.XPATH}
    TEXT_EDITOR = {'selector': '//textarea', 'by': By.XPATH}

    @staticmethod
    def get_table_field(day=0, column=1, row=1):
        """Get x-path selector of a field from diary records table

        :param day: day of week (0 - Monday, 5 - Saturday)
        :param column: 1 - subject, 2 - record's text
        :param row: number of lesson from 1 to 7 inclusive

        :return: dict with x-path selector and selector type
        """
        selector = '//div[@view_id="daytable{}"]/div[@class="webix_ss_body"]' \
                   '/div[@class="webix_ss_center"]/div[@class="webix_ss_center_scroll"]' \
                   '/div[@column="{}"]/div[@aria-rowindex="{}"]'.format(day, column, row)
        return {'selector': selector, 'by': By.XPATH}

    def test_diary(self):
        """Diary web interface testing scenario
        """
        self.login(settings.USER_STUDENT['username'],
                   settings.USER_STUDENT['password'])
        self.open(settings.DIARY_URL)
        self.wait_for_ready_state_complete()
        try:
            logging.info('Waiting for web interface...')
            self.assertEqual(_('Diary'), self.get_page_title())
            self.wait_for_element(**self.DATEPICKER)
            for i in range(6):
                field = self.get_table_field(day=i, column=2, row=7)
                self.wait_for_element(**field)
            logging.info('Done')
            subject_field = self.get_table_field(day=4, column=1, row=7)
            text_field = self.get_table_field(day=4, column=2, row=7)
            subject = data_test_api_diary.template['subject']
            text = 'Sample text for testing purposes'
            logging.info('Set new subject "{}"'.format(subject))
            self.double_click(**subject_field)
            self.find_element(**self.SUBJECT_SELECT).send_keys(
                subject + Keys.ENTER)
            msg = self.wait_for_element(**self.MESSAGE).text
            self.assertEqual(_('Record saved'), msg)
            logging.info('Passed')
            logging.info('Set new record text: {}'.format(text))
            self.double_click(**text_field)
            self.find_element(**self.TEXT_EDITOR).send_keys(text + Keys.ENTER)
            msg = self.wait_for_element(**self.MESSAGE).text
            self.assertEqual(_('Record saved'), msg)
            logging.info('Passed')
            logging.info('Diary record saved')
        except Exception as e:
            logging.error('Error during creating diary record')
            logging.error(e)
            self.fail(e)


if __name__ == '__main__':
    pytest.main()
