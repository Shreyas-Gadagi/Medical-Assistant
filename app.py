import time
import numpy as np 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from neo4j_driver import run_query
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from PIL import Image

from streamlit_chat import message
from streamlit.components.v1 import html
from english2results import get_results
from timeit import default_timer as timer
# from htmlTemplates import css, bot_template, user_template
st.set_page_config(
    page_title="Cogwise Medical Assistant",
    layout="wide",
)



def creds_entered():
    if st.session_state['User'].strip() == 'gatecorpus.com' and st.session_state['Password'].strip() == 'cogwise.ai':
        st.session_state['authenticated'] = True
    else:
        st.session_state['authenticated'] = False
        if not st.session_state['Password']:
            st.warning("Please enter password")
        elif not st.session_state['User']:
            st.warning("Please enter username")
        else:
            st.error('Invalid Username/Passowrd')

def authenticate_user():
    c1,c2,c3=st.columns([2,100,2])
    with c1:
        logo = st.image("images/cogwise_logo.svg", width=200)
    with c2:
        pass
    with c3:
        pass
    if 'authenticated' not in st.session_state:
        # with st.form('login form'):
        #     st.text_input(label='Username',value="",key='User',on_change=creds_entered)
        #     st.text_input(label='Password',value="",key='Password',type='password',on_change=creds_entered)
            
        #     submitted = st.form_submit_button("Submit")
        #     if submitted:
        #         pass

        with st.form("my_form"):
            st.text_input(label='Username',value="",key='User')
            st.text_input(label='Password',value="",key='Password',type='password')

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit",on_click=creds_entered)
            
                
                
        return False
       

    else:
        if st.session_state['authenticated']:
            logo.image('images/bg.png')
            return True

        else:
            with st.form("my_form"):
                st.text_input(label='Username',value="",key='User')
                st.text_input(label='Password',value="",key='Password',type='password')

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit",on_click=creds_entered)
            return False
if authenticate_user():
    

    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
        </style>
        <div style='text-align: center; font-size: 2.5rem; font-weight: 600; font-family: "Roboto"; color: #21618C; line-height:1; '>Cogwise Medical Assistant</div>
        <div style='text-align: center; font-size: 1rem; font-weight: 300; font-family: "Roboto"; color: rgb(179 185 182); line-height:0; '>
            Powered by <img src="https://uploads-ssl.webflow.com/6491a373b88c5c47294ab3ed/64929fb15674f58481bb955a_Asset%207.svg" alt="Custom Logo" style="height:30px; padding-left:5px; padding-right:8px"><svg width="80" height="60" xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 200 75"><path d="M39.23,19c-10.58,0-17.68,6.16-17.68,18.11v8.52A8,8,0,0,1,25,44.81a7.89,7.89,0,0,1,3.46.8V37.07c0-7.75,4.28-11.73,10.8-11.73S50,29.32,50,37.07V55.69h6.89V37.07C56.91,25.05,49.81,19,39.23,19Z"/><path d="M60.66,37.8c0-10.87,8-18.84,19.27-18.84s19.13,8,19.13,18.84v2.53H67.9c1,6.38,5.8,9.93,12,9.93,4.64,0,7.9-1.45,10-4.56h7.6c-2.75,6.66-9.27,10.94-17.6,10.94C68.63,56.64,60.66,48.67,60.66,37.8Zm31.15-3.62c-1.38-5.73-6.08-8.84-11.88-8.84S69.5,28.53,68.12,34.18Z"/><path d="M102.74,37.8c0-10.86,8-18.83,19.27-18.83s19.27,8,19.27,18.83-8,18.84-19.27,18.84S102.74,48.67,102.74,37.8Zm31.59,0c0-7.24-4.93-12.46-12.32-12.46S109.7,30.56,109.7,37.8,114.62,50.26,122,50.26,134.33,45.05,134.33,37.8Z"/><path d="M180.64,62.82h.8c4.42,0,6.08-2,6.08-7V20.16h6.89v35.2c0,8.84-3.48,13.4-12.32,13.4h-1.45Z"/><path d="M177.2,59.14h-6.89V50.65H152.86A8.64,8.64,0,0,1,145,46.2a7.72,7.72,0,0,1,.94-8.16L161.6,17.49a8.65,8.65,0,0,1,15.6,5.13V44.54h5.17v6.11H177.2ZM151.67,41.8a1.76,1.76,0,0,0-.32,1,1.72,1.72,0,0,0,1.73,1.73h17.23V22.45a1.7,1.7,0,0,0-1.19-1.68,2.36,2.36,0,0,0-.63-.09,1.63,1.63,0,0,0-1.36.73L151.67,41.8Z"/><path d="M191,5.53a5.9,5.9,0,1,0,5.89,5.9A5.9,5.9,0,0,0,191,5.53Z" fill="#018bff"/><path d="M24.7,47a5.84,5.84,0,0,0-3.54,1.2l-6.48-4.43a6,6,0,0,0,.22-1.59A5.89,5.89,0,1,0,9,48a5.81,5.81,0,0,0,3.54-1.2L19,51.26a5.89,5.89,0,0,0,0,3.19l-6.48,4.43A5.81,5.81,0,0,0,9,57.68a5.9,5.9,0,1,0,5.89,5.89A6,6,0,0,0,14.68,62l6.48-4.43a5.84,5.84,0,0,0,3.54,1.2A5.9,5.9,0,0,0,24.7,47Z" fill="#018bff"/></svg> | 
        
        
        </div>
    """, unsafe_allow_html=True)

    # st.markdown("<h1 style='text-align: center; color: #21618C;'>Cogwise Medical Assistant</h1>", unsafe_allow_html=True)
    st.markdown('   ')

    with st.sidebar:
        st.sidebar.image(r"C:\Users\shara\Desktop\neo4j_application\images\cogwise_logo.svg", width=250)
        st.markdown('   ')
        st.markdown('   ')
        choice = option_menu(
            menu_title = 'Main Menu',
            options = ['Bloom','Chat','Visualizaion','About'],
            icons = ['house','book','bar-chart-line','envelope'],
            menu_icon = 'cast',
            default_index = 0,
            # orientation='horizontal',
            styles={
                # "container": {"padding": "0!important", "background-color": "#fafafa"},
                # "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#B7DBF4"},
                "nav-link-selected": {"background-color": "#21618C"}
            }
        )
        
        st.markdown('   ')
        st.markdown('   ')

        st.markdown("<h1 style='text-align: center; color: #21618C;'>About Cogwise</h1>", unsafe_allow_html=True)

        st.write(
                """
                We help organizations design and build applications and solutions that use generative 
                AI and LLMs to accelerate business value and drive growth.
                """)
        st.markdown("[Learn More>](http://www.cogwise.ai//)")

    if choice == 'Visualizaion':
        @st.cache_data
        def get_data() -> pd.DataFrame:
            return run_query("""
            MATCH (n:Case) return n.id as Id, 
            n.summary as Summary ORDER BY Id""")

        df_cases = get_data()
        placeholder = st.empty()

        with placeholder.container():
                df_diseases = run_query("""MATCH (n:Disease) return n.name as name""")
                df_body_systems = run_query("""MATCH (n:BodySystem) return n.name as name""")
                df_patients = run_query("""MATCH (n:Person) return n.id as name""")

                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                kpi1.metric(
                    label="Cases",
                    value=len(df_cases)
                )
                kpi2.metric(
                    label="Patients",
                    value=len(df_patients)
                )
                kpi3.metric(
                    label="Diseases",
                    value=len(df_diseases)
                )    
                kpi4.metric(
                    label="Body Systems",
                    value=len(df_body_systems)
                )
            
                ep_team_col = st.columns(1)
                st.markdown("### Patients, Diseases & Affected Body Parts (Top N)")
                
                df_te_1 = run_query("""
                    MATCH (e:BodySystem) 
                    return e.id as id, e.name as label, '#33a02c' as color""")
                df_te_1 = pd.DataFrame(df_te_1)
                df_te_2 = run_query("""
                    MATCH (t:Disease) 
                    return t.id as id, t.name as label, '#1f78b4' as color""")
                df_te_2 = pd.DataFrame(df_te_2)
                df_te_3 = run_query("""
                    MATCH (t:Person) 
                    return t.id as id, t.id + ' (' + t.gender + ')' as label, '#fdbf6f' as color""")
                df_te_3 = pd.DataFrame(df_te_3)
                df_te = pd.concat([df_te_1, df_te_2], ignore_index=True)
                df_te = pd.concat([df_te, df_te_3], ignore_index=True)
                df_dis_bs = run_query("""
                    MATCH (:Person)-[:HAS_DISEASE]->(d:Disease)-[a:AFFECTS]->(t:BodySystem)
                    return DISTINCT t.id as source, d.id as target, count(a) as value, 
                        '#a6cee3' as link_color LIMIT 50""")
                df_dis_bs = pd.DataFrame(df_dis_bs)
                df_dis_patient = run_query(f"""
                    MATCH (p:Person)-[:HAS_DISEASE]->(d:Disease)-[a:AFFECTS]->(t:BodySystem)
                    WHERE t.id in [{','.join(f"'{x}'" for x in df_dis_bs['source'])}]
                    return d.id as source, p.id as target, count(d) as value, 
                        '#fdbf6f' as link_color LIMIT 50""")
                df_dis_patient = pd.DataFrame(df_dis_patient)
                df_dis_bs_patient = pd.concat([df_dis_bs, df_dis_patient], ignore_index=True)
                label_mapping = dict(zip(df_te['id'], df_te.index))
                df_dis_bs_patient['src_id'] = df_dis_bs_patient['source'].map(label_mapping)
                df_dis_bs_patient['target_id'] = df_dis_bs_patient['target'].map(label_mapping)
                
                sankey = go.Figure(data=[go.Sankey(
                    arrangement="snap",
                    node = dict(
                        pad = 15,
                        thickness = 20,
                        line = dict(
                            color = "black",
                            width = 0.4
                        ),
                        label = df_te['label'].values.tolist(),
                        color = df_te['color'].values.tolist(),
                        ),
                    link = dict(
                        source = df_dis_bs_patient['src_id'].values.tolist(),
                        target = df_dis_bs_patient['target_id'].values.tolist(),
                        value = df_dis_bs_patient['value'].values.tolist(),
                        color = df_dis_bs_patient['link_color'].values.tolist()
                    )
                )])
                st.plotly_chart(sankey, use_container_width=True)

                team_col = st.columns(1)
                st.markdown("### Top Symptoms")
                df_teams = run_query("""
                    MATCH (e:Person)-[n:HAS_SYMPTOM]->(p:Symptom) 
                    return DISTINCT p.description as symptom, count(n) as occurences
                    ORDER BY occurences DESC LIMIT 10""")
                size_max_default = 7
                scaling_factor = 5
                fig_team = px.scatter(df_teams, x="symptom", y="occurences",
                            size="occurences", color="symptom",
                                hover_name="symptom", log_y=True, 
                                size_max=size_max_default*scaling_factor)
                st.plotly_chart(fig_team, use_container_width=True)

                # create two columns for charts
                fig_col1, fig_col2 = st.columns(2)
                with fig_col1:
                    st.markdown("### Most Diagnoses")
                    df = run_query("""
                    MATCH (e:Person)-[:HAS_DIAGNOSIS]->(p:Diagnosis) 
                    return DISTINCT p.name as diagnosis, count(e) as diagnoses
                    ORDER BY diagnoses DESC LIMIT 10""")
                    fig = px.scatter(df, x="diagnosis", y="diagnoses",
                            size="diagnoses", color="diagnosis",
                                    hover_name="diagnosis", log_y=True, 
                                    size_max=size_max_default*scaling_factor)
                    st.plotly_chart(fig, use_container_width=True)
                    
                with fig_col2:
                    st.markdown("### Top Diseases")
                    df = run_query("""
                    MATCH (e:Person)-[:HAS_DISEASE]->(p:Disease) 
                    return p.name as disease, count(e) as occurences
                    ORDER BY occurences DESC LIMIT 10""")
                    fig2 = px.scatter(df, x="disease", y="occurences",
                            size="occurences", color="disease",
                                    hover_name="disease", log_y=True, 
                                    size_max=size_max_default*scaling_factor)
                    st.plotly_chart(fig2, use_container_width=True)
                

    if choice == 'Bloom':
        st.markdown('   ')

        @st.cache_data
        def get_data() -> pd.DataFrame:
            return run_query("""
            MATCH (n:Case) return n.id as Id, 
            n.summary as Summary ORDER BY Id""")

        df_cases = get_data()
        placeholder = st.empty()
        with placeholder.container():
            df_diseases = run_query("""MATCH (n:Disease) return n.name as name""")
            df_body_systems = run_query("""MATCH (n:BodySystem) return n.name as name""")
            df_patients = run_query("""MATCH (n:Person) return n.id as name""")

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric(
                    label="Patients",
                    value=len(df_cases)
                )
            kpi2.metric(
                    label="Cases",
                    value=len(df_patients)
                )
            kpi3.metric(
                    label="Diseases",
                    value=len(df_diseases)
                )    
            kpi4.metric(
                    label="Body Systems",
                    value=len(df_body_systems)
                )

        

        placeholder = st.empty()
        neo4j = "https://workspace-preview.neo4j.io/workspace/explore"
        components.iframe(neo4j, width = 1150, height = 800)

        with st.expander('See Query'):
            st.write('match (n)-[r]->(m) return n,r,m')
            st.write('MATCH (n:Disease) return n.name as name')
            st.write('MATCH (n:BodySystem) return n.name as name')
            st.write('MATCH (n:Person) return n.id as name')

    if choice == 'Chat':

        

        # Hardcoded UserID
        USER_ID = "bot"
        def generate_context(prompt, context_data='generated'):
            context = []
            # If any history exists
            if st.session_state['generated']:
                # Add the last three exchanges
                size = len(st.session_state['generated'])
                for i in range(max(size-3, 0), size):
                    context.append(st.session_state['user_input'][i])
                    if len(st.session_state[context_data]) > i:
                        context.append(st.session_state[context_data][i])
            # Add the latest user prompt
            context.append(str(prompt))
            return context


        # Generated natural language
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        # Neo4j database results
        if 'database_results' not in st.session_state:
            st.session_state['database_results'] = []
        # User input
        if 'user_input' not in st.session_state:
            st.session_state['user_input'] = []
        # Generated Cypher statements
        if 'cypher' not in st.session_state:
            st.session_state['cypher'] = []


        def get_text():
            input_text = st.chat_input(
                "Ask any Question", key="input")
            return input_text


        # Define columns
        col1, col2 = st.columns([2, 1])

        with col2:
            another_placeholder = st.empty()
        with col1:
            placeholder = st.empty()
        user_input = get_text()


        if user_input:
            start = timer()
            try:
                results = get_results(generate_context(user_input, 'database_results'))
                cypher_step = results['intermediate_steps']
                print('Total Time : {}'.format(timer() - start))
                if len(cypher_step) > 0 and 'query' in cypher_step[0]:
                    st.session_state.cypher.append(cypher_step[0]['query'])
                else :
                    st.session_state.cypher.append('')
                if len(cypher_step) > 1 and 'context' in cypher_step[1] and len(cypher_step[1]['context']) > 0:
                    st.session_state.database_results.append(cypher_step[1]['context'][0])
                else:
                    st.session_state.database_results.append('')
                st.session_state.user_input.append(user_input)
                st.session_state.generated.append(results['result'])
            except Exception as ex:
                print(ex)
                st.session_state.user_input.append(user_input)
                st.session_state.generated.append("Could not generate result due to an error or LLM Quota exceeded")
                st.session_state.cypher.append("")
                st.session_state.database_results.append('{}')


        # Message placeholder
        # c_logo = r"C:\Users\shara\Desktop\neo4j_application\images\cogwise_logo.svg"
        # # cogwise = st.image(r"C:\Users\shara\Desktop\neo4j_application\images\cogwise_logo.svg", width=10)
        # cogwise = r'C:\Users\shara\Desktop\neo4j_application\images\cg_logo.png'
        # c=st.image(cogwise, width=70)
        with placeholder.container():
            if st.session_state['generated']:
                size = len(st.session_state['generated'])
                # Display only the last three exchanges
                for i in range(max(size-3, 0), size):
                    message(st.session_state['user_input'][i],
                            is_user=True, key=str(i) + '_user',avatar_style="initials", seed="User")
                    message(st.session_state["generated"][i], key=str(i),avatar_style='initials',seed='Cg')

                    


        # Generated Cypher statements
        with another_placeholder.container():
            if st.session_state['cypher']:
                st.text_area("Latest generated Cypher statement",
                            st.session_state['cypher'][-1], height=240)
            
        with st.expander("Sample Questions"):
            st.write("1.Which patient has the most number of symptoms?")
            st.write('2.Which disease affect most of my patients?')
            st.write('3.How many of my patients suffer from both cough and weight loss?')
            st.write('4.When someone has cough and nausea, do they also lose weight?')
            st.write('5.Which body part got affected in most of my patients?')
            st.write('6.Which age group has the most number of heart diseases?')
                

        # st.markdown("---")

        # st.markdown("""
        # <style>
        # table {
        #     width: 100%;
        #     border-collapse: collapse;
        #     border: none !important;
        #     font-family: "Source Sans Pro", sans-serif;
        #     color: rgba(49, 51, 63, 0.6);
        #     font-size: 0.9rem;
        # }

        # tr {
        #     border: none !important;
        # }
        
        # th {
        #     text-align: center;
        #     colspan: 3;
        #     border: none !important;
        #     color: #0F9D58;
        # }
        
        # th, td {
        #     padding: 2px;
        #     border: none !important;
        # }
        # </style>

        # <table>
        # <tr>
        #     <th colspan="3">Sample Questions to try out</th>
        # </tr>
        # <tr>
        #     <td>Which patient has the most number of symptoms?</td>
        #     <td>Which disease affect most of my patients?</td>
        #     <td>How many of my patients suffer from both cough and weight loss?</td>
        # </tr>
        # <tr>
        #     <td>When someone has cough and nausea, do they also lose weight?</td>
        #     <td>Which body part got affected in most of my patients?</td>
        #     <td>Which age group has the most number of heart diseases?</td>
        # </tr>
        # </table>
        # """, unsafe_allow_html=True)

    if choice == 'About':
        from PIL import Image
        st.markdown("""
        This is a application which shows howOpenAI can be used with Neo4j to build and consume Knowledge Graphs using unstructured Medical Transcript Corpus.
        Using OpenAI GPT-4 model, medical transcript text is converted to Knowledge Graph.
                    
        The Sample Case History text used in this demo looks like:
                    
        ```
        A 28-year-old woman was referred with a 4-week history of continuous, moderate right upper quadrant pain associated with jaundice, as well as weight loss (10 kg over 3 months) and a liver mass identified by ultrasonography.
        The pain sensation seemed different from previous colicky attacks the patient had experienced before she underwent laparoscopic cholecystectomy 7 years previously.
        On physical examination, she was obese (body mass index 37.8), with icterus noted over the conjunctivae, oral mucosa and skin.
        Imaging modalities included computed tomography (CT), positron emission tomography (PET) and endoscopic cholangiopancreatography (ERCP) (Fig.1).
        The patient underwent exploratory laparotomy.
        Intraoperative ultrasonography revealed a cystic lesion measuring 3.5 2.5 cm within the central portion of the liver, anterior to the porta hepatis.
        Intraoperative cholangiography demonstrated an extensive stricture obliterating the left hepatic duct, with partial occlusion of the right hepatic duct.
        An extended left lobectomy was done en bloc with the biliary confluence.
        On frozen-section examination, all margins of the excised specimen were free of malignant cells.
        Reconstruction was performed with a Roux-en-Y cholangiojejunostomy to 3 second bile duct radicals in the right side.
        Intraoperatively, radiotherapy was applied to the surgical margins.
        After this, the patient underwent 6 weeks of image-guided external beam radiation centred on the resection field labelled at surgery.
        The final pathology described this tumour as an infiltrating, moderately differentiated squamous cell carcinoma associated with severe dysplasia of the bile-duct epithelium (Fig.2).
        The patient recovered without complications and was doing well 18 months after the initial surgical procedure, with an unremarkable CT scan.
        ```

        ### Why Neo4j is a great addition to LLMs:
        - *Fine-grained access control of your data* : You can control who can and cannot access parts of your data
        - Greater reliability with factual data
        - More Explainability
        - Domain specificity
        - Ability to gain insights using Graph Algorithms
        - Vector embedding support and Similarity Algorithms on Neo4j

        """, unsafe_allow_html=True)

        arch = Image.open('./images/arch.png')
        langchain = Image.open('./images/langchain-neo4j.png')
        schema = Image.open('./images/schema.png')

        st.image(arch)
        st.markdown("""
        ---

        This the schema in which the transformed data are stored in Neo4j
        """)
        st.image(schema)
        st.markdown("""
        ---

        This is how the Chatbot flow goes:
        """)
        st.image(langchain)

