# Schoolmate - school management system
# Copyright (C) 2018-2019  Kirill 'Kolyat' Kiselnikov  <kks.pub@gmail.com>
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

from datetime import date, time, timedelta


FORM_LETTERS = 'АБ'
SUBJECTS = [
    'Русский язык',
    'Английский язык',
    'Немецкий язык',
    'Французский язык',
    'Литература',
    'Английская литература',
    'Математика',
    'Алгебра',
    'Геометрия',
    'Информатика',
    'Технология',
    'Окружающий мир',
    'Обществознание',
    'ОРКСЭ',
    'ОДНКНР',
    'Искусство',
    'Музыка',
    'ИЗО',
    'Физическая культура',
    'История',
    'География',
    'Физика',
    'Химия',
    'Биология',
    'ОБЖ',
    'История города',
    'Астрономия',
    'Электив (русский язык)',
    'Электив (обществознание)',
    'Электив (математика)',
    'Электив (физика)',
    'Электив (история)'
].__reversed__()
DAILY_SCHEDULE = [
    {
        'number': 1,
        'period_type': 'L',
        'start_time': time(9, 0, 0),
        'end_time': time(9, 45, 0),
        'description': '1 урок'
    },
    {
        'number': 1,
        'period_type': 'B',
        'start_time': time(9, 45, 1),
        'end_time': time(9, 55, 0),
        'description': '1 перемена'
    },
    {
        'number': 2,
        'period_type': 'L',
        'start_time': time(9, 55, 1),
        'end_time': time(10, 40, 0),
        'description': '2 урок'
    },
    {
        'number': 2,
        'period_type': 'B',
        'start_time': time(10, 40, 1),
        'end_time': time(10, 55, 0),
        'description': '2 перемена'
    },
    {
        'number': 3,
        'period_type': 'L',
        'start_time': time(10, 55, 1),
        'end_time': time(11, 40, 0),
        'description': '3 урок'
    },
    {
        'number': 3,
        'period_type': 'B',
        'start_time': time(11, 40, 1),
        'end_time': time(12, 0, 0),
        'description': '3 перемена'
    },
    {
        'number': 4,
        'period_type': 'L',
        'start_time': time(12, 0, 1),
        'end_time': time(12, 45, 0),
        'description': '4 урок'
    },
    {
        'number': 4,
        'period_type': 'B',
        'start_time': time(12, 45, 1),
        'end_time': time(13, 5, 0),
        'description': '4 перемена'
    },
    {
        'number': 5,
        'period_type': 'L',
        'start_time': time(13, 5, 1),
        'end_time': time(13, 50, 0),
        'description': '5 урок'
    },
    {
        'number': 5,
        'period_type': 'B',
        'start_time': time(13, 50, 1),
        'end_time': time(14, 0, 0),
        'description': '5 перемена'
    },
    {
        'number': 6,
        'period_type': 'L',
        'start_time': time(14, 0, 1),
        'end_time': time(14, 45, 0),
        'description': '6 урок'
    },
    {
        'number': 6,
        'period_type': 'B',
        'start_time': time(14, 45, 1),
        'end_time': time(15, 0, 0),
        'description': '6 перемена'
    },
    {
        'number': 7,
        'period_type': 'L',
        'start_time': time(15, 0, 1),
        'end_time': time(15, 45, 0),
        'description': '7 урок'
    }
].__reversed__()
SCHOOL_YEAR = {
    'name': '2019-2020',
    'start_date': date(2019, 9, 1),
    'end_date': date(2020, 5, 25)
}
YEAR_SCHEDULE = [
    {
        'number': 1,
        'period_type': 'Q',
        'start_date': SCHOOL_YEAR['start_date'],
        'end_date': date(2019, 10, 26),
        'description': 'I четверть'
    },
    {
        'number': 1,
        'period_type': 'H',
        'start_date': date(2019, 10, 27),
        'end_date': date(2019, 11, 3),
        'description': 'Осенние каникулы'
    },
    {
        'number': 2,
        'period_type': 'Q',
        'start_date': date(2019, 11, 4),
        'end_date': date(2019, 12, 28),
        'description': 'II четверть'
    },
    {
        'number': 2,
        'period_type': 'H',
        'start_date': date(2019, 12, 29),
        'end_date': date(2020, 1, 12),
        'description': 'Зимние каникулы'
    },
    {
        'number': 3,
        'period_type': 'Q',
        'start_date': date(2020, 1, 13),
        'end_date': date(2020, 3, 22),
        'description': 'III четверть'
    },
    {
        'number': 3,
        'period_type': 'H',
        'start_date': date(2020, 3, 23),
        'end_date': date(2020, 3, 31),
        'description': 'Весенние каникулы'
    },
    {
        'number': 4,
        'period_type': 'Q',
        'start_date': date(2020, 4, 1),
        'end_date': SCHOOL_YEAR['end_date'],
        'description': 'IV четверть'
    },
    {
        'number': 4,
        'period_type': 'H',
        'start_date': SCHOOL_YEAR['end_date'] + timedelta(days=1),
        'end_date': SCHOOL_YEAR['start_date'] - timedelta(days=1),
        'description': 'Летние каникулы'
    },
    {
        'number': 5,
        'period_type': 'H',
        'start_date': date(2020, 2, 4),
        'end_date': date(2020, 2, 10),
        'description': 'Дополнительные каникулы для первоклассников'
    }
].__reversed__()
CLASSROOMS = [{'room_id': i, 'room_name': '{} кабинет'.format(i)}
              for i in range(1, 50)]
