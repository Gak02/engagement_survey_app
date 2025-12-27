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

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .score-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .score-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .interpretation-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

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
SCALE_OPTIONS = {
    0: "0 - 全くない",
    1: "1 - 1年に数回以下",
    2: "2 - 1ヶ月に1回以下",
    3: "3 - 1ヶ月に数回",
    4: "4 - 1週間に1回",
    5: "5 - 1週間に数回",
    6: "6 - 毎日",
}

# スコア解釈の基準（Schaufeli & Bakkerの基準を参考）
def get_score_level(score):
    if score < 1.0:
        return "非常に低い", "#e74c3c"
    elif score < 2.5:
        return "低い", "#e67e22"
    elif score < 3.5:
        return "やや低い", "#f39c12"
    elif score < 4.5:
        return "平均的", "#3498db"
    elif score < 5.5:
        return "高い", "#27ae60"
    else:
        return "非常に高い", "#16a085"

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
    values.append(values[0])  # レーダーチャートを閉じるため
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
    
    colors = [get_score_level(s)[1] for s in scores.values()]
    
    fig = px.bar(
        df, 
        x="項目", 
        y="スコア",
        color="項目",
        color_discrete_sequence=colors,
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
    level, _ = get_score_level(total)
    
    interpretations = {
        "非常に低い": """
        ワークエンゲージメントが非常に低い状態です。仕事に対するエネルギーや意欲が
        著しく低下している可能性があります。職場環境や業務内容の見直し、
        上司や同僚との対話、専門家への相談を検討することをお勧めします。
        """,
        "低い": """
        ワークエンゲージメントが低めの状態です。仕事への活力や熱意を
        取り戻すために、業務の優先順位の見直しや、達成感を得られる
        小さな目標設定から始めてみることをお勧めします。
        """,
        "やや低い": """
        ワークエンゲージメントがやや低い状態です。仕事の意義や
        やりがいを再確認し、強みを活かせる業務に注力することで、
        エンゲージメントの向上が期待できます。
        """,
        "平均的": """
        ワークエンゲージメントは平均的なレベルです。現状を維持しながら、
        より充実した仕事経験を得るために、新しいチャレンジや
        スキルアップの機会を探してみてはいかがでしょうか。
        """,
        "高い": """
        ワークエンゲージメントが高い状態です。仕事に対して
        ポジティブな感情を持ち、活力に満ちた状態と言えます。
        この良い状態を維持するために、適度な休息も大切にしてください。
        """,
        "非常に高い": """
        ワークエンゲージメントが非常に高い状態です。仕事に対して
        強い情熱とエネルギーを持っています。素晴らしい状態ですが、
        燃え尽き症候群を防ぐため、ワークライフバランスにも注意を払いましょう。
        """
    }
    
    return interpretations.get(level, "")

# メイン画面
def main():
    st.markdown('<p class="main-header">📊 ワークエンゲージメント診断</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">UWES-9（ユトレヒト・ワーク・エンゲイジメント尺度）</p>', unsafe_allow_html=True)
    
    # セッションステートの初期化
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # タブの作成
    tab1, tab2, tab3 = st.tabs(["📝 診断", "📈 結果", "ℹ️ UWESについて"])
    
    with tab1:
        st.markdown("### 回答方法")
        st.info("""
        以下の9つの質問について、あなたが仕事に関してそのように感じる頻度を選択してください。
        すべての質問に回答後、「結果を見る」ボタンをクリックしてください。
        """)
        
        st.markdown("---")
        
        responses = {}
        
        for q_num, q_data in QUESTIONS.items():
            st.markdown(f"**Q{q_num}. {q_data['text']}**")
            st.caption(f"📌 サブスケール: {q_data['subscale']}")
            
            response = st.select_slider(
                f"q{q_num}",
                options=list(SCALE_OPTIONS.keys()),
                format_func=lambda x: SCALE_OPTIONS[x],
                value=st.session_state.responses.get(q_num, 3),
                key=f"slider_{q_num}",
                label_visibility="collapsed"
            )
            responses[q_num] = response
            st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 結果を見る", use_container_width=True, type="primary"):
                st.session_state.responses = responses
                st.session_state.submitted = True
                st.rerun()
    
    with tab2:
        if st.session_state.submitted and st.session_state.responses:
            scores = calculate_scores(st.session_state.responses)
            
            st.markdown("### 📊 あなたの診断結果")
            st.caption(f"診断日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
            
            # スコアカード
            col1, col2 = st.columns(2)
            
            with col1:
                total_level, total_color = get_score_level(scores["総合スコア"])
                st.markdown(f"""
                <div class="score-card" style="background: linear-gradient(135deg, {total_color} 0%, {total_color}99 100%);">
                    <div class="score-label">総合スコア</div>
                    <div class="score-value">{scores["総合スコア"]:.2f}</div>
                    <div class="score-label">{total_level}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                subscale_html = ""
                for name, score in list(scores.items())[:-1]:
                    level, color = get_score_level(score)
                    subscale_html += f"<div style='margin: 0.3rem 0;'><strong>{name.split(' ')[0]}:</strong> {score:.2f} ({level})</div>"
                
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; height: 100%;">
                    <div style="font-weight: bold; margin-bottom: 0.5rem;">サブスケール別スコア</div>
                    {subscale_html}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
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
            st.markdown(f'<div class="interpretation-box">{interpretation}</div>', unsafe_allow_html=True)
            
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
            st.markdown("---")
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
            
            # リセットボタン
            if st.button("🔄 もう一度診断する"):
                st.session_state.submitted = False
                st.session_state.responses = {}
                st.rerun()
        
        else:
            st.info("👈 「診断」タブで質問に回答してから、こちらで結果を確認できます。")
    
    with tab3:
        st.markdown("""
        ### ワークエンゲージメントとは
        
        ワークエンゲージメントとは、仕事に対するポジティブで充実した心理状態を指します。
        オランダ・ユトレヒト大学のSchaufeli教授らによって提唱された概念で、
        バーンアウト（燃え尽き症候群）の対極に位置づけられています。
        
        ### UWES-9について
        
        UWES（Utrecht Work Engagement Scale）は、ワークエンゲージメントを測定する
        国際的に最も広く使用されている尺度です。本診断では9項目版（UWES-9）を使用しています。
        
        ### 3つのサブスケール
        
        | サブスケール | 説明 | 質問番号 |
        |------------|------|---------|
        | **活力 (Vigor)** | 仕事中の高い水準のエネルギーや心理的な回復力 | Q1, Q2, Q5 |
        | **熱意 (Dedication)** | 仕事への強い関与、意義・熱意・誇りの感覚 | Q3, Q4, Q7 |
        | **没頭 (Absorption)** | 仕事に集中し、没頭している状態 | Q6, Q8, Q9 |
        
        ### スコアの解釈目安
        
        | スコア範囲 | レベル |
        |-----------|--------|
        | 0.0 - 0.9 | 非常に低い |
        | 1.0 - 2.4 | 低い |
        | 2.5 - 3.4 | やや低い |
        | 3.5 - 4.4 | 平均的 |
        | 4.5 - 5.4 | 高い |
        | 5.5 - 6.0 | 非常に高い |
        
        ### 出典・参考文献
        
        - Schaufeli, W.B., & Bakker, A.B. (2003). UWES – Utrecht Work Engagement Scale
        - 島津明人 (2014). ワーク・エンゲイジメント：ポジティブ・メンタルヘルスで活力ある毎日を
        
        ---
        
        ⚠️ **注意事項**
        
        本診断は、学術研究目的で開発されたUWES-9に基づいています。
        営利目的での使用には著者の許可が必要です。
        結果は参考情報であり、専門的な診断に代わるものではありません。
        """)

    # フッター
    st.markdown("---")
    st.caption("© Schaufeli & Bakker (2003) - UWES-9 Japanese Version")

if __name__ == "__main__":
    main()