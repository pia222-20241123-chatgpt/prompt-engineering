from datetime import datetime
import pandas as pd
df = pd.read_csv('d:/bs_lists.csv')

# 이전 아이디를 추적하고, 변경 시점을 출력
previous_id = None

for idx,current_id in enumerate(df.id):
    if previous_id != current_id:  # 아이디가 변경되었을 때
        print(f"아이디가 변경되었습니다: {current_id} (인덱스 {idx})")
    previous_id = current_id    
    print(df.loc[idx,'id'],df.loc[idx,'psw'],df.loc[idx,'business_no'])

#  현재년도

current_year = datetime.now().year
print(current_year-1)

print(len(df))
    