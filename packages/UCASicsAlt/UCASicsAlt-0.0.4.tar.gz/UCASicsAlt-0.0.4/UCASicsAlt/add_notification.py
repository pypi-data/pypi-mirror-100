import click
import re


@click.command()
@click.option('-t', '--time', default=30, help='提前发出通知的时间分钟数')
@click.option('-s', '--source', default='schedule.ics', help='要修改的ics文件路径')
def cli(time, source):
    time_reg = re.compile(r'\d{8}T\d{6}')
    record = []
    records = []
    target = open('./result.ics', 'w', encoding='utf-8')
    flag = False
    with open(source, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        for index in range(len(lines)):
            if lines[index] == 'BEGIN:VEVENT\n':
                record.append(index)
                flag = True
            if lines[index][:7] == 'SUMMARY':
                record.append(lines[index])
            if lines[index][:7] == 'DTSTART' and flag:
                # record.append(lines[index])
                tmp = re.findall(time_reg, lines[index])
                record.append([int(tmp[0][:8]), int(tmp[0][9:])])
            if lines[index] == 'END:VEVENT\n':
                record.append(index)
                records.append(record)
                record = []
        last_class_name = records[0][1]
        last_class_index = 0
        cnt = 1
        for index_lines in range(records[0][0]):
            target.write(lines[index_lines])
        for index in range(len(records)):
            # print(records[index])
            if ((records[index][2] == last_class_name and records[index][1][0] == records[index - 1][1][0]) and
                    ((records[index][1][1] - records[index - 1][1][1]) < 11001)):

                cnt += 1
            else:
                if cnt < 3:
                    duration = 'DURATION:PT' + str(cnt * 50) + 'M\n'
                else:
                    duration = 'DURATION:PT' + str(cnt * 50 + 20) + 'M\n'
                for index_lines in range(records[last_class_index][0], records[last_class_index][3]):
                    if lines[index_lines][0:8] != 'DURATION':
                        target.write(lines[index_lines])
                    else:
                        target.write(duration)
                target.write(
                    'BEGIN:VALARM\nTRIGGER:-PT' + str(time) + 'M\nACTION:DISPLAY\nDESCRIPTION:\nEND:VALARM\n')
                target.write('END:VEVENT\n')
                cnt = 1
                last_class_name = records[index][2]
                last_class_index = index
    target.close()
