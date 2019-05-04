import csv


class CSVReader:
    def load_csv_and_extract_feature(self, file_name, indexes, label):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            data = []
            for row in csv_reader:
                if line_count != 0:
                    data.append([float(row[i]) for i in indexes])
                line_count += 1
            return data
