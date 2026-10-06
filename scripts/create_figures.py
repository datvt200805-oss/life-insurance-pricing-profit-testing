"""Tạo hai hình dùng cho README; không ảnh hưởng kết quả định phí."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/"results"/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def main():
    out=ROOT/"reports/figures"
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11})
    scenarios=read("python_scenarios.csv")
    labels=["Cơ sở","Tử vong +10%","Hủy +25%","Chi phí +10%","Chiết khấu -1 điểm %","Kết hợp"]
    fig,ax=plt.subplots(figsize=(10,4.7),layout="constrained")
    values=[float(r["profit_margin"])*100 for r in scenarios]
    bars=ax.barh(labels,values,color=["#244C73"]+["#668EB1"]*5)
    ax.invert_yaxis()
    ax.axvline(0,color="#9AA6B2",lw=.8)
    ax.axvline(10,color="#A86A25",lw=1,ls="--",label="Mục tiêu cơ sở: 10%")
    for b,v in zip(bars,values):
        ax.text(v+(0.25 if v>=0 else -0.25),b.get_y()+b.get_height()/2,f"{v:.2f}%",va="center",ha="left" if v>=0 else "right")
    ax.set_xlim(min(values)-3,max(values)+3)
    ax.set_xlabel("PV profit / PV premium (%)")
    ax.set_title("Thay đổi profit margin khi giữ nguyên phí cơ sở",loc="left",pad=15)
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="lower right",frameon=False)
    fig.savefig(out/"scenario_margin.png",dpi=160)
    plt.close(fig)
    rows=[r for r in read("python_annual.csv") if r["scenario_id"]=="1"]
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(10,7),layout="constrained",sharex=True)
    years=[int(r["year"]) for r in rows]
    for field,label,color in (("premium_cashflow","Phí thu","#244C73"),("claims","Quyền lợi tử vong","#B06B3B"),("maintenance_expense","Chi phí duy trì","#648C67")):
        ax1.plot(years,[float(r[field])/1000 for r in rows],label=label,color=color,lw=2)
    ax1.set_ylabel("Nghìn VND / hợp đồng ban đầu")
    ax1.set_title("Dòng tiền kỳ vọng trong 20 năm — kịch bản cơ sở",loc="left")
    ax1.legend(frameon=False)
    ax2.bar(years,[float(r["pv_profit"])/1000 for r in rows],color="#668EB1")
    ax2.axhline(0,color="#9AA6B2",lw=.8)
    ax2.set_ylabel("PV dòng tiền thuần (nghìn VND)")
    ax2.set_xlabel("Năm hợp đồng")
    ax2.set_xticks(range(1,21))
    for ax in (ax1,ax2): ax.spines[["top","right"]].set_visible(False)
    fig.savefig(out/"base_cashflows.png",dpi=160)
    plt.close(fig)

if __name__=="__main__": main()
