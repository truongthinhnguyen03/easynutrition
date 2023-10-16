import streamlit as st
from langchain import PromptTemplate, LLMChain, HuggingFaceHub

st.title('🦜🔗 Easy Nutrition')

HUGGINGFACEHUB_API_TOKEN = st.sidebar.text_input('HuggingFace API Token')
## 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
## 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

def generate_response(input_text):
  template = """
  You are a nutritionist;
  You are given an ingredient list;
  You can generate an EXPLANATION using simple term to explain the possible origin of each ingredient
  and what type of food this ingredient list comes from.

  LIST: {input_text}
  EXPLAINATION:
  """

  prompt = PromptTemplate(template=template, input_variables=['input_text'])

  repo_id = "HuggingFaceH4/zephyr-7b-alpha"

  llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"max_new_tokens":256, "do_sample":True, "temperature":0.7, "top_k":50, "top_p":0.95}
  )

  llm_chain = LLMChain(prompt=prompt, llm=llm)

  st.info(llm_chain.run(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'Sugar, Invert sugar, corn syrup, modified corn starch, citric acid, tartaric acid, natural and artificial flavour, titanium dioxide, red 40, yellow 5, and blue 1')
  submitted = st.form_submit_button('Submit')
  if not HUGGINGFACEHUB_API_TOKEN.startswith('hf-'):
    st.warning('Please enter your HuggingFace API key!', icon='⚠')
  if submitted and HUGGINGFACEHUB_API_TOKEN.startswith('hf-'):
    generate_response(text)
    