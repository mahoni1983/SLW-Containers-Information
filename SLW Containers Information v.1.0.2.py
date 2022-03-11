import tkinter as tk
#import tkinter.scrolledtext as tkscrolledtext
import pyodbc
import decimal
from tabulate import tabulate
import pyperclip #UNCOMMENT before compilation to have copy clipboard function working
"""
Releases history:
SLW Containers Information v.1.0.2:
added MS SQL and MS ACCESS queries separation
"""
#True =  to run with building window, not as console. False - to run as console (not tested after window mode added. Worked before widow mode.
b_run_as_window_not_as_console = True
#Window icon, can not be included into runnable one-file EXE.
#window_icon = "barrel_icon.ico"
program_name = "SLW Containers Information v.1.0.2"
about_program_text = [program_name + "\nThe program is designed to work at Ignalina Nuclear Power Plant.\n"
                      "It shows information about sent for storage concrete containers filled with short-live radioactive waste.\n"
                      "The program connects to Tracking database, collects and represents information for all sent for storage concrete containers or for a single container (for entered barcode).\n\n"
                      "Used programming language: Python.\n\n"
                      "Developer: Jevgenij Kariagin\n"
                      "email: mahoni1983@mail.ru\n"
                      "2020-05",
                      program_name + "\nПрограмма предназначена для работы на Игналинской атомной электростанции.\n"
                      "Показывает информацию о бетонных контейнерах, наполненных короткоживущими радиоактивными отходами, отправленных в хранилище.\n"
                      "Программа подсоединяется к базе данных Tracking комплекса по переработке радиоактивных отходов, собирает и показывает информацию по всем бетонным контейнерам, отправленным в хранилище, или по одному контейнеру (по введённому штрих-коду).\n"
                      "Язык программирования: Python.\n\n"
                      "Разработчик: Евгений Карягин\n"
                      "email: mahoni1983@mail.ru\n"
                      "2020-05"]
# connector to Access db or Tracking.
connector = None
# version="v.1.0.1"
# path to Access file. The program connects first to it.
path_to_mdb = "D:\\работа\\2020-03-10.mdb"
# used for console. language is English or not.
b_language_en = True
current_language_id = 0  # 0- English, 1 - Russian
# not used. for using dict in lang switching
#current_status_key = None
#  current status for switching lang.
current_status_id = 0
# to use query to Access or to MS SQL
b_connected_to_MS_Access = False
# query to get info for btn_current for MS Access
query_curent_Access = "SELECT StorageX_Cont as X, StorageY_Cont as Y, StorageZ_Cont as Z, ID_Cont as Container , " \
                "IIF(Drums_count is not Null AND T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null, 'Mixed', " \
                "IIF(Drums_count is not Null, 'Drums', IIF(T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null, " \
                "'Bulk', '')))  as waste_type , MassBrutto_Cont as mass_brutto, MassNetto_MST10CMS as " \
                "mass_netto , DateGrout_Cont as date_grouted, 	Drums_count, Drums_Mass_in_kg, 	Drums_Volume_in_m3, " \
                "DRSMean_MST10CMS as DR_mean	, DRSMax_MST10CMS as DR_max, EndDate_MST10CMS as MST10_measured, " \
                "Remarks_Cont as remarks from (select ID_Cont, MeasID_MST072_Cont, MeasID_MST100_Cont, DateGrout_Cont, " \
                "Remarks_Cont, StorageX_Cont, StorageY_Cont, StorageZ_Cont, MassBrutto_Cont, EndDate_MST10CMS, 	" \
                "	MassNetto_MST10CMS	, DRSMean_MST10CMS	, DRSMax_MST10CMS FROM T_Cont INNER JOIN T_MST10CMS on " \
                "T_Cont.MeasID_MST100_Cont = T_MST10CMS.ID_MST10CMS where Type_Cont = 1) as T_Cont_join_T_MST10CMS " \
                "LEFT JOIN UserView_TST16_ContInfo on T_Cont_join_T_MST10CMS.ID_Cont = " \
                "UserView_TST16_ContInfo.Container ORDER BY StorageX_Cont, StorageY_Cont, StorageZ_Cont "
# query to get info for btn_current for MS SQL
query_curent_MsSql = "SELECT StorageX_Cont as X, StorageY_Cont as Y, StorageZ_Cont as Z, ID_Cont as Container, " \
                     "CASE WHEN Drums_count is not Null AND T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null THEN " \
                     "'Mixed' ELSE CASE WHEN Drums_count is not Null THEN 'Drums' ELSE CASE WHEN " \
                     "T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null THEN 'Bulk' ELSE '' END END END as " \
                     "waste_type , MassBrutto_Cont as mass_brutto , MassNetto_MST10CMS as mass_netto , DateGrout_Cont " \
                     "as date_grouted, Drums_count, Drums_Mass_in_kg, Drums_Volume_in_m3, DRSMean_MST10CMS as DR_mean, " \
                     "DRSMax_MST10CMS as DR_max, EndDate_MST10CMS as MST10_measured, Remarks_Cont as remarks from (" \
                     "select ID_Cont, MeasID_MST072_Cont, MeasID_MST100_Cont, DateGrout_Cont, Remarks_Cont, " \
                     "StorageX_Cont, StorageY_Cont, StorageZ_Cont, MassBrutto_Cont, EndDate_MST10CMS, 	" \
                     "	MassNetto_MST10CMS	, DRSMean_MST10CMS	, DRSMax_MST10CMS FROM T_Cont INNER JOIN T_MST10CMS on " \
                     "T_Cont.MeasID_MST100_Cont = T_MST10CMS.ID_MST10CMS where Type_Cont = 1) as " \
                     "T_Cont_join_T_MST10CMS LEFT JOIN UserView_TST16_ContInfo on T_Cont_join_T_MST10CMS.ID_Cont = " \
                     "UserView_TST16_ContInfo.Container ORDER BY StorageX_Cont, StorageY_Cont, StorageZ_Cont "
#in (select ID_Cont from T_Cont where lastAction_Cont = 700700) "
# query to get info for btn_custom for MS Access
query_custom_Access = "SELECT StorageX_Cont as X, StorageY_Cont as Y, StorageZ_Cont as Z, ID_Cont as Container , " \
                "IIF(Drums_count is not Null AND T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null, 'Mixed', " \
                "IIF(Drums_count is not Null, 'Drums', IIF(T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null, " \
                "'Bulk', '')))  as waste_type , MassBrutto_Cont as mass_brutto, MassNetto_MST10CMS as " \
                "mass_netto , DateGrout_Cont as date_grouted, 	Drums_count, Drums_Mass_in_kg, 	Drums_Volume_in_m3, " \
                "DRSMean_MST10CMS as DR_mean	, DRSMax_MST10CMS as DR_max, EndDate_MST10CMS as MST10_measured, " \
                "Remarks_Cont as remarks from (select ID_Cont, MeasID_MST072_Cont, MeasID_MST100_Cont, DateGrout_Cont, " \
                "Remarks_Cont, StorageX_Cont, StorageY_Cont, StorageZ_Cont, MassBrutto_Cont, EndDate_MST10CMS, 	" \
                "	MassNetto_MST10CMS	, DRSMean_MST10CMS	, DRSMax_MST10CMS FROM T_Cont INNER JOIN T_MST10CMS on " \
                "T_Cont.MeasID_MST100_Cont = T_MST10CMS.ID_MST10CMS where Type_Cont = 1 AND ID_Cont = $to_replace$) as T_Cont_join_T_MST10CMS " \
                "LEFT JOIN UserView_TST16_ContInfo on T_Cont_join_T_MST10CMS.ID_Cont = " \
                "UserView_TST16_ContInfo.Container ORDER BY StorageX_Cont, StorageY_Cont, StorageZ_Cont "
# query to get info for btn_custom for MS SQL
query_custom_MsSql = "SELECT StorageX_Cont as X, StorageY_Cont as Y, StorageZ_Cont as Z, ID_Cont as Container, " \
                     "CASE WHEN Drums_count is not Null AND T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null THEN " \
                     "'Mixed' ELSE CASE WHEN Drums_count is not Null THEN 'Drums' ELSE CASE WHEN " \
                     "T_Cont_join_T_MST10CMS.MeasID_MST072_Cont is not Null THEN 'Bulk' ELSE '' END END END as " \
                     "waste_type , MassBrutto_Cont as mass_brutto , MassNetto_MST10CMS as mass_netto , DateGrout_Cont " \
                     "as date_grouted, Drums_count, Drums_Mass_in_kg, Drums_Volume_in_m3, DRSMean_MST10CMS as DR_mean, " \
                     "DRSMax_MST10CMS as DR_max, EndDate_MST10CMS as MST10_measured, Remarks_Cont as remarks from (" \
                     "select ID_Cont, MeasID_MST072_Cont, MeasID_MST100_Cont, DateGrout_Cont, Remarks_Cont, " \
                     "StorageX_Cont, StorageY_Cont, StorageZ_Cont, MassBrutto_Cont, EndDate_MST10CMS, 	" \
                     "	MassNetto_MST10CMS	, DRSMean_MST10CMS	, DRSMax_MST10CMS FROM T_Cont INNER JOIN T_MST10CMS on " \
                     "T_Cont.MeasID_MST100_Cont = T_MST10CMS.ID_MST10CMS where Type_Cont = 1 AND ID_Cont = $to_replace$) as " \
                     "T_Cont_join_T_MST10CMS LEFT JOIN UserView_TST16_ContInfo on T_Cont_join_T_MST10CMS.ID_Cont = " \
                     "UserView_TST16_ContInfo.Container ORDER BY StorageX_Cont, StorageY_Cont, StorageZ_Cont "
# to represent answer from SQL in appropriate form for two lang.
list_columns = [
    ["X", "Y", "Z", "Container", "waste_type", "mass_brutto", "mass_netto", "date_grouted", "Drums_count", "Drums_Mass_in_kg", "Drums_Volume_in_m3", "DR_mean", "DR_max", "MST10_measured", "remarks"],
    ["X", "Y", "Z", "Container", "Waste type", "Mass brutto,\n kg", "Mass netto,\n kg", "Date grouted", "Drums\n count", "Drums mass,\n kg", "Drums volume,\n m3", "DR mean,\n mSv/h", "DR max,\n mSv/h", "MST10 measured date", "Remarks"],
    ["X", "Y", "Z", "Контейнер", "Тип отходов", "Масса полная,\n кг", "Масса нетто,\n кг", "Зацементирован", "Кол-во\n бочек", "Масса бочек, \nкг", "Объём бочек, \nм3", "Ср. МЭД,\n мЗв/ч", "Макс. МЭД,\n мЗв/ч", "Дата измерения MST10", "Заметки"]
]

dict_columns_to_summ = {"Z": 'each count', "Container": 'count', "waste_type": 'each count', "mass_brutto": 'sum', "mass_netto": 'sum', "date_grouted": 'range date', "Drums_count": 'sum', "Drums_Mass_in_kg": 'sum', "Drums_Volume_in_m3": 'sum', "DR_mean": 'range', "DR_max": 'range', "MST10_measured": 'range date'}
#\
    #{"Drum": 'count', "Position": 'each count', "Loaded_date": 'range date', "Waste": 'each count', "NV": 'each count', "Height": 'sum',
     #                   "Measured_date": 'range date', "Mass_brutto": 'sum', "Mass_netto": 'sum', "DRM_mean": 'range', "DRM_max": 'range', "Co60_Bq": 'sum', "Co60_Bq_kg": 'range'}

# to format results. Column names must be as sql header
list_columns_to_format = [
    ["mass_brutto", "mass_netto", "DR_mean", "DR_max", "Drums_count", "Drums_Mass_in_kg", "Drums_Volume_in_m3"],
    [['{:.0f}'], ['{:.0f}'], ['{:.4f}'], ['{:.4f}'], ['{:.0f}'], ['{:.0f}'], ['{:.2f}']],
    []
]
# [
#     ["Height", "Mass_brutto", "Mass_netto", "DR_mean", "DR_max", "DRM1m_max", "Co60_Bq", "Co60Unc_Bq", "Co60_Bq_kg"],
#     [['{:.0f}'], ['{:.0f}'], ['{:.0f}'], ['{:.5g}'], ['{:.4f}'], ['{:.4f}'], ['{:.2E}'], ['{:.2E}'], ['{:.2E}']],
#     []
# ]

# for switching lang.
dict_controls = {'btn_about': ["About program", "О программе"],
                 'lbl_language': ["Language", "Язык"],
                 'lbl_current': ["Containers in storage", "Контейнеры в хранилище"],
                 'btn_current': ["Show info", "Получить информацию"],
                 'lbl_custom': ["Custom container (through barcode)", "Контейнер по введённому штрих-коду"],
                 'btn_custom': ["Show info", "Получить информацию"],
                 'btn_exit': ["Exit program", "Выход"],
                 'btn_copy_to_clipboard': ["Copy text to clipboard", "Скопировать текст в буфер обмена"],
                 'btn_clear': ["Clear text", "Стереть текст"],
                 # '': ["", ""],
                 }

# not used, for different lang. to choose from. Replaced by list, but dict. looks to suit better.
# dict_status = {'Connecting to Tracking database': ["Connecting to Tracking database", "Устанавливается соединение с базой данных Tracking"],
#                'Connected to Tracking database successfully': ["Connected to Tracking database successfully", "Соединение с базой данных Tracking установлено успешно"],
#                'Failed to connect to a database': ["Failed to connect to Tracking database", "Связь с базой данных Tracking не установлена"],
#                 'Connected to the MS Access database successfully': ["Connected to the MS Access database successfully", "Соединение с базой данных MS Access установлено успешно"],
#                 'Program started': ["Program started", "Программа запущена"]
#                }

# for switching lang.
list_status = [["Program started", "Программа запущена"],
               ["Connecting to Tracking database. Please wait, can take up to a minute", "Устанавливается соединение с базой данных Tracking, может занять до минуты времени."],
               ["Connected to Tracking database successfully",
                "Соединение с базой данных Tracking установлено успешно"],
               ["Failed to connect to Tracking database", "Связь с базой данных Tracking не установлена"],
               ["Connected to the MS Access database successfully",
                "Соединение с базой данных MS Access установлено успешно"],
               ["Failed to connect to Tracking database", "Нет соединения с базой данных Tracking"]
               ]

def connect_to_db():
    """connection to DB, first to Access file to path_to_mdb, second to Tracking"""
    print("connect_to_db started")
    change_status("connecting to a MS Access database")
    global b_connected_to_MS_Access
    # append_text("connecting to a MS Access database")
    try:
        try:
            connector = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path_to_mdb + ';')
            print("Connected to a MS Access database")
            # append_text("connected to the MS Access database")
            b_connected_to_MS_Access = True
            change_status("Connected to the MS Access database successfully")
        except:
            print("Connect to a MS Access database failed")
            # append_text("connecting to a SQL database")
            change_status("Connecting to Tracking database. Please wait, can take up to a minute")
            connector = pyodbc.connect('Driver={SQL Server};'
                                       'Server=GK990-a05;'
                                       'Database=TrackingDBB234;'
                                       'Trusted_Connection=yes;')
            print("Connected to Tracking database")
            append_text("connected to the SQL database")
            change_status("Connected to Tracking database successfully")
    except:
        connector = None
        print("Failed to connect to a database")
        append_text("Failed to connect to a database")
        change_status("Failed to connect to Tracking database")
    return (connector)


def get_current_time():
    import time
    secondsSinceEpoch = time.time()
    timeObj = time.localtime(secondsSinceEpoch)
    time_now = '%d-%02d-%02d %02d:%02d:%02d' % (
        timeObj.tm_year, timeObj.tm_mon, timeObj.tm_mday, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec)
    #print('Current TimeStamp is : %d-%d-%d %d:%d:%d' % (
        #timeObj.tm_mday, timeObj.tm_mon, timeObj.tm_year, timeObj.tm_hour, timeObj.tm_min, timeObj.tm_sec))
    return (time_now)

def format_single_result(result_to_format, header):
    formatted_result = result_to_format
    global list_columns_to_format
    if header in list_columns_to_format[0]:
        index = list_columns_to_format[0].index(header)
        format_for_result = list_columns_to_format[1][index]
        formatted_result = format_for_result[0].format(result_to_format)
    return formatted_result

def get_summs(results, headers_sql):
    #results_with_summs = []
    #results_with_summs = results
    new_row_to_add_to_results = []
    global dict_columns_to_summ
   # Drum, Position, Loaded_date, Waste, NV, Height, Mass_brutto, Mass_netto, DRM_mean, DRM_max, Co60_Bq, Co60_Bq_kg = None
    #for i in range(len(headers_from_results)):
        # list_columns_to_summ = ["Drum", "Position", "Loaded_date", "Waste", "NV", "Height", "Mass_brutto", "Mass_netto", "DRM_mean", "DRM_max", "Co60_Bq", "Co60_Bq_kg"]
    #for header in headers_from_results:
    for i in range(len(headers_sql)):
        #print("get_summs, header:", header[0])
        header = headers_sql[i]#[0]
        if header in dict_columns_to_summ:
            #new_row_to_add_to_results.append(dict_columns_to_summ[header])
            current_result = '-'
            try:
                if dict_columns_to_summ[header] == 'count':
                    print("do counting for", header)
                    current_result = len(results)
                    print(' result:', current_result)
                elif dict_columns_to_summ[header] == 'sum':
                    print("do summing for", header)
                    result_sum = 0.0
                    for result in results:
                        if type(result[i]) is str:
                            result_temp = float(result[i])
                        elif result[i] is None:
                            result_temp = 0.0
                        else:
                            result_temp = result[i]
                        result_sum = result_sum + result_temp
                    current_result = format_single_result(result_sum, header)
                    print(' result:', current_result)
                elif dict_columns_to_summ[header] == 'distinct':
                    print("do distinct for", header)
                    current_result = ''
                    list_current_result = []
                    for result in results:
                        if result[i] not in list_current_result:
                            list_current_result.append(result[i])
                    list_current_result.sort()
                    #current_result = list_current_result.copy()
                    for current_result_from_list in list_current_result:
                        current_result = current_result + '\n' + current_result_from_list
                    print(' result:', current_result)
                elif dict_columns_to_summ[header] == 'range':
                    print("do range for", header)
                    current_result = 'range'
                    mini = None
                    maxi = None
                    for result in results:
                        if type(result[i]) is str:
                            result_temp = float(result[i])
                        else:
                            result_temp = result[i]
                        if mini == None:
                            mini = result_temp
                            maxi = result_temp
                        if result_temp < mini: mini = result_temp
                        if result_temp > maxi: maxi = result_temp
                    mini = format_single_result(mini, header)
                    maxi = format_single_result(maxi, header)

                    current_result = '{}\n{}'.format(mini, maxi)
                    print(' result:', current_result)
                    #'{} {}'.format('one', 'two')
                elif dict_columns_to_summ[header] == 'range date':
                    print("do range date for", header)
                    current_result = 'range date'
                    mini = None
                    maxi = None
                    for result in results:
                        if result[i] is None:
                            continue
                        if mini == None:
                            mini = result[i]
                            maxi = result[i]
                        if result[i] < mini: mini = result[i]
                        if result[i] > maxi: maxi = result[i]
                    current_result = '{}\n{}'.format(mini, maxi)
                    print(' result:', current_result)
                elif dict_columns_to_summ[header] == 'each count':
                    print("do each count for", header)
                    current_result = 'each count'
                    list_current_result = []
                    list_element = []
                    list_element_count = []
                    for result in results:
                        if result[i] in list_element:
                            index = list_element.index(result[i])
                            list_element_count[index] += 1
                        else:
                            list_element.append(result[i])
                            list_element_count.append(1)
                    current_result = ''
                    for i in range(len(list_element)):
                        if i != 0:
                            current_result = current_result + '\n'
                        current_result = current_result + '{}: {}'.format(list_element[i], list_element_count[i])
                    print(' result:', current_result)
            except:
                print('Error getting sums in header:', header)
            new_row_to_add_to_results.append(current_result)
        else:
            new_row_to_add_to_results.append('-')
        #new_row_to_add_to_results.append(current_result)

    print("New row to add to results: ", new_row_to_add_to_results)
   # print(results)
    #print(results_with_summs.append(new_row_to_add_to_results))
    #results_with_summs.append(new_row_to_add_to_results)
    #print(results_with_summs)
    return new_row_to_add_to_results


def get_empty_row(headers_sql):
    empty_row = ['-'] * len(headers_sql)
    empty_row_chars_count = []
    # for header in headers:
    return empty_row


def get_operation_row(headers_sql):
    new_operation_row_to_add_to_results = []
    global dict_columns_to_summ
    # Drum, Position, Loaded_date, Waste, NV, Height, Mass_brutto, Mass_netto, DRM_mean, DRM_max, Co60_Bq, Co60_Bq_kg = None
    # for i in range(len(headers_from_results)):
    # list_columns_to_summ = ["Drum", "Position", "Loaded_date", "Waste", "NV", "Height", "Mass_brutto", "Mass_netto", "DRM_mean", "DRM_max", "Co60_Bq", "Co60_Bq_kg"]
    # for header in headers_from_results:
    for i in range(len(headers_sql)):
        # print("get_summs, header:", header[0])
        header = headers_sql[i]  # [0]
        if header in dict_columns_to_summ:
            new_operation_row_to_add_to_results.append(dict_columns_to_summ[header] + ':')
        else:
            new_operation_row_to_add_to_results.append('-')
    return(new_operation_row_to_add_to_results)

    pass


def add_totals_to_results(headers_sql, results, row_number):
    last_row_with_totals = get_summs(results, headers_sql)
    #format_results(headers_sql, last_row_with_totals)
    empty_row = get_empty_row(headers_sql)
    operation_row = get_operation_row(headers_sql)
    results.append(empty_row)
    results.append(operation_row)
    results.append(last_row_with_totals)
    #row_number = range(row_number.start, row_number.stop + 1)
    #row_number = list(row_number)  # .append(13)
    row_number.append('-')
    row_number.append('-')
    row_number.append('-')


def format_results(headers_sql, results):
    global list_columns_to_format
    if len(list_columns_to_format) == 0:
        # exit if nothing to format
        return None
    list_columns_to_format[2] = [None] * len(list_columns_to_format[0])
    results_formatted = results.copy()
    try:
        for header in headers_sql:
            if header in list_columns_to_format[0]:
                index = list_columns_to_format[0].index(header)
                list_columns_to_format[2][index] = headers_sql.index(header)
        for result in results_formatted:
            for index in list_columns_to_format[2]:
                if index != None:
                    try:
                        result[index] = list_columns_to_format[1][list_columns_to_format[2].index(index)][0].format(result[index])
                    except:
                        print('Error in format_results. Header:', headers_sql[index], ': ', result[index])
    except:
        print('Error in format_results.')
    #print(results_formatted)
    pass


def show_results(cursor, b_add_totals):
    """
    to work out with SQL results and represent according to lang. choice
    :param cursor: result from SQL
    :param b_add_totals: add totals to results, True - to add; False - not to add
    :return: result taking in an account lang. goes to text widget
    """
    global b_language_en
    global current_language_id
    global list_data
    global list_columns
    # column_number - column_from_list_columns_to_print
    column_number = 0
    if current_language_id == 0:
        column_number = 1
    elif current_language_id == 1:
        column_number = 2
    try:
        results = cursor.fetchall()
    except:
        results = []
        print('Error getting results from DB')
    print("debug: len(results): ", len(results))
    result_table = ""
    if len(results) != 0:
        headers = []
        headers_sql = []
        row_number = []
        for i in range(0, len(cursor.description)):
            header = cursor.description[i][0]
            headers_sql.append(header)
            if header in list_columns[0]:
                header_index = list_columns[0].index(header)
                header = list_columns[current_language_id+1][header_index]
            # split long header into two or more words
            #header = header.replace("_", "\n")
            headers.append(header)
            #headers.append(cursor.description[i][0]) # unsplitted header
        #row_number=list(range(1, len(results)+1))
        row_number = list(range(1, len(results)+1))

        # for header in headers:
        #     header.replace("_", "\n")
        format_results(headers_sql, results)
        if b_add_totals:
            add_totals_to_results(headers_sql, results, row_number)

        result_table = tabulate(results, headers=headers, showindex=row_number, tablefmt="orgtbl")
        print(result_table)
        # for i in range(0, len(cursor.description)):
        #     # print(i+1, '\t', cursor.description[i][0], '\t', results[0][i])
        #     parameter_name = cursor.description[i][0]
        #     if cursor.description[i][0] in list_columns[0]:
        #         row_number = list_columns[0].index(cursor.description[i][0])
        #         # print("debug row_number:", row_number)
        #         parameter_name = list_columns[column_number][row_number]
        #     # print("debug parameter_name:", parameter_name)
        #     print((str(i + 1)+'.').ljust(4) + parameter_name + ':'.ljust(3) + str(results[0][i]))
        #     result_text = result_text + (str(i + 1)+'.').ljust(4) + parameter_name + ':'.ljust(3) + str(results[0][i]) + '\n'


    else:
        print("No results returned")
        if current_language_id == 0:
            result_table = "No results returned from the database.\n"
        elif current_language_id == 1:
            result_table = "Возвращён нулевой результат из базы данных.\n"
    filled_string = "\n".ljust(result_table.index('\n')+1, '=')+"\n"
    result_table = get_current_time() + '\n' + result_table
    result_table = result_table + filled_string
    print(filled_string)
    append_text(result_table)


def show_info_about_current_container():
    """
    make connection if not connected yet, take info from db and show results (with show_results())
    :return: none
    """
    print("show_info_about_current_container() started")
    global connector
    if connector == None:
        connector = connect_to_db()
    if connector == None:  # failed to connect to DB
        append_text("Failed to connect to a DB")
    else:
        cursor = connector.cursor()
        if b_connected_to_MS_Access:
            cursor.execute(query_curent_Access)
        else:
            cursor.execute(query_curent_MsSql)
        show_results(cursor, True)

def show_info_about_custom_container(custom_container):
    """
    make connection if not connected yet, take info from db and show results (with show_results())
    :return: none
    """
    print("show_info_about_current_container() started")
    global connector
    if connector == None:  # check connected to a DB or not
        connector = connect_to_db()
    if connector == None:  # failed to connect to DB
        append_text("Failed to connect to a DB")
    else:
        cursor = connector.cursor()
        try:
            if b_connected_to_MS_Access:
                cursor.execute(query_custom_Access.replace('$to_replace$', custom_container))
            else:
                cursor.execute(query_custom_MsSql.replace('$to_replace$', custom_container))
        except:
            print('Error in executing SQL query')
        show_results(cursor, False)


def show_menu():
    """
    shows menu in console mode
    :return:
    """
    global b_language_en
    if b_language_en:
        print("-----Menu-----")
        print("1. Show info about current container on MST16")
        print("2. Show info about custom container (with bar-code)")
        print("8. Меню на русском.")
        print("9. Quit program.")
        chosen_option = input("Please choose an option: ")
    else:
        print("-----Меню-----")
        print("1. Показать информацию о текущем контейнере на MST16")
        print("2. Показать информацию о контейнере по штрих-коду")
        print("8. Menu in English.")
        print("9. Выход из программы.")
        chosen_option = input("Пожалуйста выберете пункт: ")
    print("")
    return (chosen_option)


def choice_selection(chosen_option):
    """
    for console mode. run a way from selected option
    :param chosen_option:
    :return:
    """
    global b_language_en
    try:
        if chosen_option == "1":
            print("Option 1: Showing info about current container on MST16")
            show_info_about_current_container()
        elif chosen_option == "2":
            print("Option 2")
            custom_container = input("Please type in container number: \n")
            show_info_about_custom_container(custom_container)
        elif chosen_option == "8":
            print("Option 8")
            if b_language_en:
                b_language_en = False
                print("Switching to Russian\n")
            else:
                b_language_en = True
                print("Переключаем язык на английский\n")
        elif chosen_option == "9":
            print("Option 9")
            return (True)
        else:
            print("Not correct option")
    except:
        print("Error: connection to a database failed\n")
        return None


def run_console():
    """
    to run console in console mode
    :return:
    """
    b_to_quit = False
    while not b_to_quit:
        chosen_option = show_menu()
        b_to_quit = choice_selection(chosen_option)
    print("End program")


def show_about():
    """
    shows about dialog
    :return:
    """
    print("show_about called")
    global window
    from tkinter import messagebox
    # messagebox = tk.messagebox()
    # messagebox.showinfo("Information", "Informative message")
    if current_language_id == 0:
        tk.messagebox.showinfo(title="About Program", message=about_program_text[0])  # , **options)
    elif current_language_id == 1:
        tk.messagebox.showinfo(title="О программе", message=about_program_text[1])
    # window.build_window().show_custom()
    # window.show_custom()
    # window.txt_info.insert(1.0, "about")


def exit_program():
    print("exit called")
    window.destroy()


def append_text(text):
    """
    appends text (parameter) to Text widget txt_info.
    :param text:
    :return:
    """
    global txt_info
    txt_info.configure(state='normal')
    txt_info.insert(tk.END, text + '\n')
    # global window
    # window.update()
    txt_info.see(tk.END)
    txt_info.configure(state='disabled')


def change_status(new_status_to_set_eng):
    """
    changes status taking in account lang. using list_status
    :param new_status_to_set_eng:
    :return:
    """
    global lbl_status
    global current_status_id
    new_status = new_status_to_set_eng
    if current_status_id != 'None':
        global list_status
        #new_status = new_status_to_set_eng
        for i in range(len(list_status)):
            #print('list_status[i][0] ', list_status[i][0])
            if list_status[i][0] == new_status_to_set_eng:
                new_status = list_status[i][current_language_id]
                current_status_id = i
                break
    # commented part is to work with status texts stored in dictionary
    #global current_language_id
    #new_status = 'text'
    # if text in dict_status:
    #     new_status = dict_status[text][current_language_id]
    #     global current_status_key
    #     current_status_key = text
    # else:
    #     new_status = text
    #current_status = lbl_status['text']
    # global list_status
    # new_status = new_status_to_set_eng
    # for i in range(len(list_status)):
    #     print('list_status[i][0] ', list_status[i][0])
    #     if list_status[i][0] == new_status_to_set_eng:
    #         new_status = list_status[i][current_language_id]
    #         print('new_status: ', new_status)
    #         #change_status(list_status[i][new_language_id])
    #         break
    lbl_status.config(text=new_status)

    global window
    window.update()


def show_current():
    """
    shows current container info when clicked btn_current
    :return:
    """
    print("show_current called")
    show_info_about_current_container()


def show_custom():
    """
    shows custom container info when clicked btn_custom
    :return:
    """
    print("show_custom called")
    global window
    global ent_barcode

    barcode = ent_barcode.get()
    if barcode == "":
        if current_language_id == 0:
            append_text("Please enter a barcode")
        elif current_language_id == 1:
            append_text("Введите штрих-код контейнера")
    else:
        print("barcode: ", barcode)
        if current_language_id == 0:
            append_text("entered barcode: " + barcode + '\n')
        elif current_language_id == 1:
            append_text("Введён штрих-код: " + barcode + '\n')
        show_info_about_custom_container(barcode)


# def get_all_children_widgets (parent_widget) :
#     """ gets all of the widgets within one entire window.
#     it is needed to switch language for all possible widgets"""
#     _list = parent_widget.winfo_children()
#
#     for item in _list :
#         if item.winfo_children() :
#             _list.extend(item.winfo_children())
#     return _list

def switch_language():
    """
    to switch lang.
    :return:
    """
    global var_language
    global current_language_id
    global current_status_id

    new_language_id = var_language.get()
    if current_language_id != new_language_id:
        print("changing language, old language_id: ", current_language_id)
        print("new language id: ", var_language.get())

        for key in dict_controls:
             if key in globals():
                 # print("switching language: ", key)
                 globals().get(key)['text'] = dict_controls[key][new_language_id]
        global lbl_status
      #  print(list_status.index([lbl_status['text']])[])
      #  for element in list_status[current_language_id]

        # status language change block


        current_language_id = new_language_id

        lbl_status['text'] = list_status[current_status_id][current_language_id]
        #change_status(lbl_status['text'])
        # if current_status_key != None:
        #     change_status(current_status_key)
        # else:
        #     change_status(lbl_status['text'])
    # window.update()


def clear_text():
    print("clear text started")
    # global txt_info
    txt_info.configure(state='normal')
    txt_info.delete(1.0, tk.END)
    txt_info.configure(state='disabled')

def copy_to_clipboard():
    print("copy_to_clipboard started")
    pyperclip.copy(txt_info.get("1.0",tk.END))

# Window elements
window = tk.Tk()
# window.iconbitmap(window_icon) commented as can not be included into one EXE -file.
window.geometry('+0+0')
fr1_1_2 = tk.Frame(window, borderwidth=10)
fr1 = tk.Frame(fr1_1_2, borderwidth=10)
lbl_name = tk.Label(master=fr1, text=program_name)
btn_about = tk.Button(master=fr1, text="About program", command=show_about)

fr1_2 = tk.Frame(fr1_1_2, borderwidth=10)
lbl_language = tk.Label(master=fr1_2, text="Language")
var_language = tk.IntVar()
radbtn1 = tk.Radiobutton(fr1_2, text='English', variable=var_language, value=0, command=switch_language)
radbtn2 = tk.Radiobutton(fr1_2, text='Русский', variable=var_language, value=1, command=switch_language)

fr2_3 = tk.Frame(window)
fr2 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
lbl_current = tk.Label(master=fr2, text=dict_controls['lbl_current'][current_language_id])
btn_current = tk.Button(master=fr2, text="Show info", command=show_current)
fr3 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
lbl_custom = tk.Label(master=fr3, text=dict_controls['lbl_custom'][current_language_id])
ent_barcode = tk.Entry(fr3, width=16)
btn_custom = tk.Button(master=fr3, text="Show info", command=show_custom)
lbl_status = tk.Label(master=window, text="Program started")
fr4 = tk.Frame(master=window, borderwidth=2)
txt_info = tk.Text(fr4, width=65, height=23, wrap="none", xscrollcommand=True, yscrollcommand=True)
txt_info_xscroll = tk.Scrollbar(fr4, command=txt_info.xview, orient=tk.HORIZONTAL)
txt_info_yscroll = tk.Scrollbar(fr4, command=txt_info.yview)


fr5 = tk.Frame(window, borderwidth=10)
btn_exit = tk.Button(master=fr5, text="Exit program", command=exit_program)
btn_copy_to_clipboard = tk.Button(master=fr5, text="Copy text to clipboard", command=copy_to_clipboard)
btn_clear = tk.Button(master=fr5, text="Clear text", command=clear_text)


def build_window():
    global window
    window.title(program_name)
    # window.rowconfigure(0, weight=1)
    # window.columnconfigure(0, weight=1)
    # window.columnconfigure(1, weight=1)

    #    fr1 = tk.Frame(window, borderwidth=10)
    global fr1_1_2
    global fr1
    ##fr1.columnconfigure([0, 1], minsize=100, weight=1)
    ##fr1.rowconfigure(0, minsize=100, weight=1)
    ##fr1.grid(row=0, column=0)
    global lbl_name
    # lbl_name=tk.Label(master=fr1, text=program_name)
    lbl_name.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    ##lbl1.grid(row=0, column=0, padx=5, pady=5)
    # btn_about=tk.Button(master=fr1, text="About program", command=show_about)
    global btn_about
    btn_about.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=5)

    global lbl_language
    lbl_language.pack(fill=tk.BOTH, side=tk.TOP, padx=10, pady=1)
    global radbtn1
    global radbtn2
    radbtn1.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=1)
    radbtn2.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=1)
    fr1.pack(side=tk.LEFT, expand=True)
    fr1_2.pack(side=tk.LEFT, expand=True)

    fr1_1_2.pack()#expand=True)

    # btn_exit=tk.Button(master=fr1,  text="Exit program", command=exit_program)
    #    global btn_exit                            #place to bottom
    # btn1.grid(row=0, column=1, padx=5, pady=5)
    #    btn_exit.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)                            #place to bottom

    # fr1.grid(row=0, column=0)
    # fr2.pack()

    # fr2_3 = tk.Frame(window)
    # fr2 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
    # lbl_current=tk.Label(master=fr2, text="Current container (on MST7.2)")
    global fr2_3
    global fr2
    global lbl_current
    lbl_current.pack(padx=10)
    # btn_current=tk.Button(master=fr2,  text="Show info", command=show_current)
    global btn_current
    btn_current.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=10)
    fr2.pack(side=tk.LEFT, padx=10, pady=5)

    # fr3 = tk.Frame(fr2_3, borderwidth=2, relief=tk.GROOVE)
    # lbl_custom=tk.Label(master=fr3, text="Custom container (through barcode)")
    global fr3
    global lbl_custom
    lbl_custom.pack(padx=10)
    # ent_barcode = tk.Entry(fr3, width=16)
    global ent_barcode
    ent_barcode.pack(side=tk.LEFT, padx=10)
    # btn_custom=tk.Button(master=fr3,  text="Show info", command=show_custom)
    global btn_custom
    btn_custom.pack(side=tk.RIGHT, expand=True, padx=10)
    fr3.pack(side=tk.RIGHT, pady=5)

    fr2_3.pack()

    # lbl_status=tk.Label(master=window, text="...current status...")
    global lbl_status
    lbl_status.pack(pady=5)

    # fr4 = tk.Frame(master=window, borderwidth=2)
    global fr4
    # txt_info = tk.Text(fr4, width=70, height=30, yscrollcommand=True)
    global txt_info
    txt_info.config(state="disabled")
    # txt_info.insert(1.0, "Hello.....\n")
    # txt_info.insert(1.0, "24	state	It the state is set to DISABLED, the widget becomes unresponsive\n to the mous\ne and keyboard unresponsive\n                    25	ta\nbs	This option controls how the tab character is used to position the text.\nt represents the width of the widget in characters.")
    #txt_info.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X, expand=True)
    # rowconfigure and columnconfigure added for txt_info to be expandable
    tk.Grid.rowconfigure(fr4, 0, weight=1)
    tk.Grid.columnconfigure(fr4, 0, weight=1)
    txt_info.grid(row=0, column=0, sticky="n"+"s"+"e"+"w")
    # scrollb = tk.Scrollbar(fr4, command=txt_info.yview)
    global txt_info_yscroll
    #txt_info_yscroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    txt_info_yscroll.grid(row=0, column=1, sticky="n"+"s"+"e"+"w")
    txt_info['yscrollcommand'] = txt_info_yscroll.set
    global txt_info_xscroll
    #txt_info_xscroll.pack(side=tk.BOTTOM, fill=tk.BOTH)
    txt_info_xscroll.grid(row=1, column=0, sticky="n"+"s"+"e"+"w")
    txt_info['xscrollcommand'] = txt_info_xscroll.set


    fr4.pack(fill=tk.BOTH, expand=True)

    global fr5
    global btn_exit
    global btn_clear
    btn_clear.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
    btn_copy_to_clipboard.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=5)
    btn_exit.pack(fill=tk.BOTH, side=tk.RIGHT, padx=10, pady=5)
    fr5.pack(fill=tk.X)

    window.mainloop()


# build_window() - uncomment to run as window application
if b_run_as_window_not_as_console:
    build_window()
else:
    run_console()
# run_console() - uncomment to run as console
# run_console()
