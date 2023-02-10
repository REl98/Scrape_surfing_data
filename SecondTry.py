import math
import pylab as p

# with open('file1.csv', 'r', encoding='utf8') as f:
#     reader = csv.reader(f)
#     vData = []
#     for i, line in enumerate(f):
#         if i == 2:
#             vData.append(line.strip())
#         elif i > 2:
#             break

# html = browser.page_source
# soup = BeautifulSoup(html, 'lxml')
# soup2 = soup.select('tr[id*="tabid_2_0_SMER"]')
# df = pd.DataFrame([str(p) for p in soup2], dtype=object)
# df.to_csv('file1.csv')


# splitdata = vData[0].split("span")
# splitdata2 = []
# for e in splitdata:
#     if "title" in e:
#         splitdata2.append(e[:19])
#     else:
#         pass

# df.to_csv(f'{os.path.join(os.getcwd())}/out.csv', header=False)

# def create_num(arr):
#     temp = []
#     for i in range(len(arr)):
#         if i+1 < len(arr):
#             if arr[i] and arr[i+1] != '':
#                 temp.append(arr[i]+arr[i+1])
#             else:
#                 if arr[i] == '' and arr[i+1] != '':
#                     if i+2 < len(arr):
#                         if arr[i+2] == '':
#                             temp.append(arr[i+1])
#                         else:
#                              i += 1
#                     else:
#                         temp.append(arr[i + 1])
#     return temp
