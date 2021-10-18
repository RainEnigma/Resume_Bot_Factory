from config import config


# ф-ция для получения текста из файла эксель
def text_message(row, column):
    answer = config.sheet.cell(row=row, column=column).value
    return str(answer)
