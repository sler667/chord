# Chord Canvas Demo

這是一個可放上 GitHub 的小型編曲 demo，主打：

- 輸入調性與目前和弦，推薦下一個和弦
- 依照 `J-Pop / Anime`、`Rock`、`Cinematic` 風格生成和弦進行
- 將和弦轉成純鋼琴配置
- 給一條可直接拿去 DAW 當靈感的旋律草稿

## Run

```bash
cd Extract_MOD_Frames-main/music_arranger_demo
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- 這版是規則式 demo，優先追求能跑、能互動、能快速產生草稿。
- 下一步很適合加上：
  - MIDI 匯出
  - 更多 borrowed chords / secondary dominants
  - 可切換節奏型
  - 分成 verse / pre-chorus / chorus 片段生成
