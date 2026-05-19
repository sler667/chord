# Chord Canvas Demo

這是一個可放上 GitHub 的編曲小工具 demo，現在有兩個頁面：

- `Arranger`
  - 輸入調性、風格、情緒與目前和弦
  - 推薦下一個和弦
  - 自動生成 progression
  - 顯示純鋼琴配置與簡單旋律草稿

- `Guitar`
  - 選擇 `Major` 或 `Minor` 調性
  - 在吉他指板上標出該調音階音的位置
  - 用不同顏色顯示 root 與其他音階音
  - 列出該調的自然和弦與常用吉他指法圖

## Run

```bash
cd D:\APP\try\music_arranger_demo
pip install -r requirements.txt
streamlit run app.py
```

## Current Scope

- 這版是規則式 demo，優先追求能跑、能互動、能快速產生草稿。
- 吉他和弦圖目前以常用開放和弦與基本 barre 形狀為主。
- 後續很適合再加：
  - MIDI 匯出
  - 更多 borrowed chords / secondary dominants
  - 分段生成 verse / pre-chorus / chorus
  - 更多吉他 chord voicing 與 scale pattern 模式
