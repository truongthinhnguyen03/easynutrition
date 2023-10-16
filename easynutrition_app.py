import streamlit as st
from langchain import PromptTemplate, LLMChain, HuggingFaceHub
import os
st.set_page_config(initial_sidebar_state='collapsed')

st.title('🍽️🥗🧘🏻‍♀️ Easy Nutrition - Proof of Concept')

st.markdown('''Easy Nutrition: Decode Your Food Labels! Are you ready to take control of your health? Take the first step to understanding what\'s on your plate.''')
st.divider()

with st.sidebar.form(key ='TokenForm'):
    HUGGINGFACEHUB_API_TOKEN = st.text_input('HuggingFace API Token', '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', type='password', disabled=True)    
    submitted_Token = st.form_submit_button(label = 'Submit')

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

def generate_response(input_text):
  template = """
  You are a nutritionist;
  You are given an ingredient list;
  You can generate EXPLANATION using simple terms to explain the possible origin of each ingredient - New line for each ingredient.

  LIST: {input_text}
  EXPLAINATION:
  """

  prompt = PromptTemplate(template=template, input_variables=['input_text'])

  repo_id = "HuggingFaceH4/zephyr-7b-alpha"

  llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"max_new_tokens":512, "do_sample":True, "temperature":0.7, "top_k":50, "top_p":0.95}
  )

  llm_chain = LLMChain(prompt=prompt, llm=llm)

  st.info(llm_chain.run(input_text))

examples = {
    'Example 1': 'Sugar, Invert sugar, corn syrup, modified corn starch, citric acid, tartaric acid, natural and artificial flavour, titanium dioxide, red 40, yellow 5, and blue 1',
    'Example 2': 'Enriched unbleached flour (wheat flour, malted barley flour, ascorbic acid [dough conditioner], niacin, reduced iron, thiamin mononitrate, ribflavin, folic acid), sugar, degermed yellow cornmeal, salt, leavening (baking soda, sodium acid pyrophosphate), soybean oil, honey powder, natural flavor'
  }
select_example = st.selectbox("Select an example", list(examples.keys()))

with st.form('my_form'):
  text = st.text_area('Enter nutrition list:', examples[select_example], height=150)
  submitted = st.form_submit_button('Submit')
  if not HUGGINGFACEHUB_API_TOKEN.startswith('hf_'):
    st.warning('Please enter your HuggingFace API key!', icon='⚠')
  if submitted and HUGGINGFACEHUB_API_TOKEN.startswith('hf_'):
    generate_response(text)
