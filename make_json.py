# SAP 전일재고 Excel → data.json 변환 스크립트
import pandas as pd
import json
import sys
import os
from datetime import date
from tkinter import Tk, filedialog, messagebox

def main():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="SAP 전일재고 파일 선택",
        filetypes=[("Excel 파일", "*.xlsx *.xls *.xlsm")]
    )
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{e}")
        return

    # 보유기한 컬럼 계산 (없으면 Aging으로 계산)
    if '보유기한' not in df.columns and 'Aging(일)' in df.columns:
        def calc_bh(ag):
            if ag >= 180: return '180일이상'
            elif ag >= 90: return '90일이상'
            elif ag >= 60: return '60일이상'
            else: return '60일미만'
        df['보유기한'] = df['Aging(일)'].apply(calc_bh)

    # 내수만 필터
    if '판매경로' in df.columns:
        df = df[df['판매경로'] == '내수']

    # 필요한 컬럼만
    cols = {
        '영업사원': 'emp',
        '공장': 'fac',
        '지종명': 'prod',
        '색상': 'color',
        '평량': 'bw',
        '가로': 'w',
        '길이': 'len',
        '거래선': 'cust',
        'Aging(일)': 'aging',
        '보유기한': 'bh',
        '재고중량(ton)': 'wt'
    }

    missing = [k for k in cols if k != 'Aging(일)' and k not in df.columns]
    if missing:
        messagebox.showerror("오류", f"컬럼을 찾을 수 없습니다:\n{missing}")
        return

    rows = []
    for _, r in df.iterrows():
        row = {}
        for kr, en in cols.items():
            if kr in df.columns:
                v = r[kr]
                if en in ('bw', 'w', 'len', 'aging'):
                    row[en] = int(v) if pd.notna(v) else 0
                elif en == 'wt':
                    row[en] = round(float(v), 2) if pd.notna(v) else 0.0
                else:
                    row[en] = str(v) if pd.notna(v) else ''
        rows.append(row)

    output = {
        "date": str(date.today()),
        "rows": rows
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    messagebox.showinfo("완료", f"data.json 생성 완료!\n총 {len(rows)}건")

if __name__ == '__main__':
    main()
