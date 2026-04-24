import streamlit as st
from logic import get_team_probability

st.set_page_config(page_title="World Cup Predictor AI")

st.title("⚽ World Cup Predictor AI")
st.write("Ask a question about a team's chances of winning the World Cup.")

user_input = st.text_input("Enter your question:")

if user_input:
    result = get_team_probability(user_input)

    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader(f"📊 {result['team']}")

        st.write(f"**Win Probability:** {result['win_probability']}")
        st.write(f"**Confidence Level:** {result['confidence_level']}")
        st.write(f"**Category:** {result['category']}")

        st.write("### Explanation")
        st.write(result["explanation"])