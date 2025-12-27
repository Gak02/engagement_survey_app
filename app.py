import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="ワークエンゲージメント診断",
    page_icon="📊",
    layout="centered"
)

# 質問項目の定義
QUESTIONS = {
    1: {"text": "仕事をしていると、活力がみなぎるように感じる", "subscale": "活力"},
    2: {"text": "職場では、元気が出て精力的になるように感じる", "subscale": "活力"},
    3: {"text": "仕事に熱心である", "subscale": "熱意"},
    4: {"text": "仕事は、私に活力を与えてくれる", "subscale": "熱意"},
    5: {"text": "朝に目がさめると、さあ仕事へ行こう、という気持ちになる", "subscale": "活力"},
    6: {"text": "仕事に没頭しているとき、幸せだと感じる", "subscale": "没頭"},
    7: {"text": "自分の仕事に誇りを感じる", "subscale": "熱意"},
    8: {"text": "私は仕事にのめり込んでいる", "subscale": "没頭"},
    9: {"text": "仕事をしていると、つい夢中になってしまう", "subscale": "没頭"},
}

# 回答選択肢
SCALE_OPTIONS = [
    "0 - 全くない",
    "1 - 1年に数回以下",
    "2 - 1ヶ月に1回以下",
    "3 - 1ヶ月に数回",
    "4 - 1週間に1回",
    "5 - 1週間に数回",
    "6 - 毎日",
]

def get_score_from_option(option):
    """選択肢からスコア（数値）を抽出"""
    return int(option.split(" - ")[0])

def get_score_level(score):
    """スコア解釈の基準"""
    if score < 1.0:
        return "非常に低い"
    elif score < 2.5:
        return "低い"
    elif score < 3.5:
        return "やや低い"
    elif score < 4.5:
        return "平均的"
    elif score < 5.5:
        return "高い"
    else:
        return "非常に高い"

def calculate_scores(responses):
    """サブスケールと総合スコアを計算"""
    vigor_items = [1, 2, 5]
    dedication_items = [3, 4, 7]
    absorption_items = [6, 8, 9]
    
    vigor_score = sum(responses[i] for i in vigor_items) / len(vigor_items)
    dedication_score = sum(responses[i] for i in dedication_items) / len(dedication_items)
    absorption_score = sum(responses[i] for i in absorption_items) / len(absorption_items)
    total_score = sum(responses.values()) / len(responses)
    
    return {
        "活力 (Vigor)": vigor_score,
        "熱意 (Dedication)": dedication_score,
        "没頭 (Absorption)": absorption_score,
        "総合スコア": total_score
    }

def create_radar_chart(scores):
    """レーダーチャートを作成"""
    categories = ["活力", "熱意", "没頭"]
    values = [
        scores["活力 (Vigor)"],
        scores["熱意 (Dedication)"],
        scores["没頭 (Absorption)"]
    ]
    values.append(values[0])
    categories.append(categories[0])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(31, 119, 180, 0.3)',
        line=dict(color='#1f77b4', width=2),
        name='あなたのスコア'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 6],
                tickvals=[0, 1, 2, 3, 4, 5, 6]
            )
        ),
        showlegend=False,
        margin=dict(l=80, r=80, t=40, b=40),
        height=400
    )
    
    return fig

def create_bar_chart(scores):
    """棒グラフを作成"""
    df = pd.DataFrame({
        "項目": list(scores.keys()),
        "スコア": list(scores.values())
    })
    
    fig = px.bar(
        df, 
        x="項目", 
        y="スコア",
        color="項目",
        text=df["スコア"].round(2)
    )
    
    fig.update_layout(
        yaxis_range=[0, 6],
        showlegend=False,
        height=350,
        yaxis_title="スコア (0-6)",
        xaxis_title=""
    )
    
    fig.update_traces(textposition='outside')
    
    return fig

def get_interpretation(scores):
    """スコアに基づく解釈を生成"""
    total = scores["総合スコア"]
    level = get_score_level(total)
    
    interpretations = {
        "非常に低い": "ワークエンゲージメントが非常に低い状態です。仕事に対するエネルギーや意欲が著しく低下している可能性があります。職場環境や業務内容の見直し、上司や同僚との対話、専門家への相談を検討することをお勧めします。",
        "低い": "ワークエンゲージメントが低めの状態です。仕事への活力や熱意を取り戻すために、業務の優先順位の見直しや、達成感を得られる小さな目標設定から始めてみることをお勧めします。",
        "やや低い": "ワークエンゲージメントがやや低い状態です。仕事の意義ややりがいを再確認し、強みを活かせる業務に注力することで、エンゲージメントの向上が期待できます。",
        "平均的": "ワークエンゲージメントは平均的なレベルです。現状を維持しながら、より充実した仕事経験を得るために、新しいチャレンジやスキルアップの機会を探してみてはいかがでしょうか。",
        "高い": "ワークエンゲージメントが高い状態です。仕事に対してポジティブな感情を持ち、活力に満ちた状態と言えます。この良い状態を維持するために、適度な休息も大切にしてください。",
        "非常に高い": "ワークエンゲージメントが非常に高い状態です。仕事に対して強い情熱とエネルギーを持っています。素晴らしい状態ですが、燃え尽き症候群を防ぐため、ワークライフバランスにも注意を払いましょう。"
    }
    
    return interpretations.get(level, "")

def show_survey():
    """診断画面を表示"""
    st.markdown("### 📝 診断")
    st.info("以下の9つの質問について、あなたが仕事に関してそのように感じる頻度を選択してください。")
    
    st.divider()
    
    responses = {}
    
    for q_num, q_data in QUESTIONS.items():
        st.markdown(f"**Q{q_num}. {q_data['text']}**")
        
        response = st.radio(
            f"Q{q_num}の回答",
            options=SCALE_OPTIONS,
            index=None,
            key=f"radio_{q_num}",
            label_visibility="collapsed"
        )
        
        if response is not None:
            responses[q_num] = get_score_from_option(response)
        else:
            responses[q_num] = None
        
        st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 結果を見る", use_container_width=True, type="primary"):
            unanswered = [q for q, r in responses.items() if r is None]
            if unanswered:
                st.error(f"⚠️ Q{', Q'.join(map(str, unanswered))} が未回答です。すべての質問に回答してください。")
            else:
                st.session_state.responses = responses
                st.session_state.page = "result"
                st.rerun()

def show_result():
    """結果画面を表示"""
    scores = calculate_scores(st.session_state.responses)
    
    st.markdown("### 📊 あなたの診断結果")
    st.caption(f"診断日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    
    st.divider()
    
    # 総合スコア表示
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        total_level = get_score_level(scores["総合スコア"])
        st.metric(
            label="総合スコア",
            value=f"{scores['総合スコア']:.2f}",
            delta=total_level
        )
    
    st.divider()
    
    # サブスケール別スコア
    st.markdown("#### サブスケール別スコア")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vigor_level = get_score_level(scores["活力 (Vigor)"])
        st.metric(
            label="活力 (Vigor)",
            value=f"{scores['活力 (Vigor)']:.2f}",
            delta=vigor_level
        )
    
    with col2:
        dedication_level = get_score_level(scores["熱意 (Dedication)"])
        st.metric(
            label="熱意 (Dedication)",
            value=f"{scores['熱意 (Dedication)']:.2f}",
            delta=dedication_level
        )
    
    with col3:
        absorption_level = get_score_level(scores["没頭 (Absorption)"])
        st.metric(
            label="没頭 (Absorption)",
            value=f"{scores['没頭 (Absorption)']:.2f}",
            delta=absorption_level
        )
    
    st.divider()
    
    # グラフ
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### レーダーチャート")
        st.plotly_chart(create_radar_chart(scores), use_container_width=True)
    
    with col2:
        st.markdown("#### スコア比較")
        st.plotly_chart(create_bar_chart(scores), use_container_width=True)
    
    # 解釈
    st.markdown("### 💡 結果の解釈")
    interpretation = get_interpretation(scores)
    st.info(interpretation)
    
    # 詳細データ
    with st.expander("📋 回答詳細データ"):
        detail_data = []
        for q_num, response in st.session_state.responses.items():
            detail_data.append({
                "質問番号": f"Q{q_num}",
                "質問内容": QUESTIONS[q_num]["text"],
                "サブスケール": QUESTIONS[q_num]["subscale"],
                "回答": response,
                "回答ラベル": SCALE_OPTIONS[response].split(" - ")[1]
            })
        st.dataframe(pd.DataFrame(detail_data), use_container_width=True, hide_index=True)
    
    # データエクスポート
    st.divider()
    st.markdown("### 📥 データエクスポート")
    
    export_data = {
        "診断日時": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "総合スコア": scores["総合スコア"],
        "活力スコア": scores["活力 (Vigor)"],
        "熱意スコア": scores["熱意 (Dedication)"],
        "没頭スコア": scores["没頭 (Absorption)"],
    }
    for q_num, response in st.session_state.responses.items():
        export_data[f"Q{q_num}"] = response
    
    df_export = pd.DataFrame([export_data])
    csv = df_export.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="📄 CSVでダウンロード",
        data=csv,
        file_name=f"uwes_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    # リセットボタン
    if st.button("🔄 もう一度診断する", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def show_about():
    """UWESについての説明を表示"""
    st.markdown("### ℹ️ UWESについて")
    
    st.markdown("#### ワークエンゲージメントとは")
    
    st.write("""
    ワークエンゲージメントとは、仕事に対するポジティブで充実した心理状態を指します。
    オランダ・ユトレヒト大学のSchaufeli教授らによって提唱された概念で、
    バーンアウト（燃え尽き症候群）の対極に位置づけられています。
    """)
    
    st.markdown("#### UWES-9について")
    
    st.write("""
    UWES（Utrecht Work Engagement Scale）は、ワークエンゲージメントを測定する
    国際的に最も広く使用されている尺度です。本診断では9項目版（UWES-9）を使用しています。
    """)
    
    st.markdown("#### 3つのサブスケール")
    
    subscale_df = pd.DataFrame({
        "サブスケール": ["活力 (Vigor)", "熱意 (Dedication)", "没頭 (Absorption)"],
        "説明": [
            "仕事中の高い水準のエネルギーや心理的な回復力",
            "仕事への強い関与、意義・熱意・誇りの感覚",
            "仕事に集中し、没頭している状態"
        ],
        "質問番号": ["Q1, Q2, Q5", "Q3, Q4, Q7", "Q6, Q8, Q9"]
    })
    st.dataframe(subscale_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### スコアの解釈目安")
    
    score_df = pd.DataFrame({
        "スコア範囲": ["0.0 - 0.9", "1.0 - 2.4", "2.5 - 3.4", "3.5 - 4.4", "4.5 - 5.4", "5.5 - 6.0"],
        "レベル": ["非常に低い", "低い", "やや低い", "平均的", "高い", "非常に高い"]
    })
    st.dataframe(score_df, use_container_width=True, hide_index=True)
    
    st.markdown("#### 出典・参考文献")
    
    st.write("""
    - Schaufeli, W.B., & Bakker, A.B. (2003). UWES – Utrecht Work Engagement Scale
    - 島津明人 (2014). ワーク・エンゲイジメント：ポジティブ・メンタルヘルスで活力ある毎日を
    """)
    
    st.divider()
    
    st.warning("""
    **⚠️ 注意事項**
    
    本診断は、学術研究目的で開発されたUWES-9に基づいています。
    営利目的での使用には著者の許可が必要です。
    結果は参考情報であり、専門的な診断に代わるものではありません。
    """)
    
    st.divider()
    
    if st.button("📝 診断を始める", use_container_width=True, type="primary"):
        st.session_state.page = "survey"
        st.rerun()

# メイン処理
def main():
    st.title("📊 ワークエンゲージメント診断")
    st.caption("UWES-9（ユトレヒト・ワーク・エンゲイジメント尺度）")
    
    # セッションステートの初期化
    if 'page' not in st.session_state:
        st.session_state.page = "survey"
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # サイドバーでナビゲーション
    with st.sidebar:
        st.markdown("### メニュー")
        
        if st.button("📝 診断", use_container_width=True):
            st.session_state.page = "survey"
            st.rerun()
        
        if st.button("📈 結果", use_container_width=True):
            if st.session_state.responses:
                st.session_state.page = "result"
                st.rerun()
            else:
                st.warning("先に診断を完了してください")
        
        if st.button("ℹ️ UWESについて", use_container_width=True):
            st.session_state.page = "about"
            st.rerun()
        
        st.divider()
        st.caption("© Schaufeli & Bakker (2003)")
        st.caption("UWES-9 Japanese Version")
    
    # ページ表示
    if st.session_state.page == "survey":
        show_survey()
    elif st.session_state.page == "result":
        if st.session_state.responses:
            show_result()
        else:
            st.warning("まだ診断が完了していません。")
            if st.button("📝 診断を始める", type="primary"):
                st.session_state.page = "survey"
                st.rerun()
    elif st.session_state.page == "about":
        show_about()

if __name__ == "__main__":
    main()
