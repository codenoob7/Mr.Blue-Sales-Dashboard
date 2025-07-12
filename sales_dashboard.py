from streamlit import sidebar
import streamlit as st
import altair as alt
import pandas as pd
import json

#Page Setup
st.set_page_config(
    page_title="Mr.Blue Sales Dashboard",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="expanded",
)
alt.theme.enable("dark")

#Data
with open('data/month_details.json','r') as f:
    data = json.load(f)
months_list = list(data.keys())

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.sidebar.image('Images/logo.png',width=150)
st.sidebar.title('Sales Dashboard')

selected_month = st.sidebar.selectbox("Select Month",months_list)
selected_format = st.sidebar.selectbox("Select Format",['Weekly Data','Daily Data'])
selected_index = months_list.index(selected_month)
if selected_index > 0:
    previous_month = months_list[selected_index - 1]
else:
    previous_month = selected_month

st.title(f'{selected_month} Summary')
st.markdown(
    """
    <div style="display:flex; justify-content:top;">
        <div style="width:100%; height:2px; background-color:#6E6E6E; margin: auto;"></div>
    </div>
    """,
    unsafe_allow_html=True
)

#Get Details
#--------Current Month-----------
sales = data[selected_month]['Revenue']
orders = data[selected_month]['Total Orders']
cst = data[selected_month]['Total Customers']
cst_in_month = data[selected_month]['Total Customers in Month']
new_cst = data[selected_month]['New Customers']
repeating_cst = data[selected_month]['Repeating Customers']
retention_rate = data[selected_month]['Overall Ret.Rate']
last_month_rr = data[selected_month]['Ret.Rate wrt. Last Month']
repeating_cst_from_last_month = data[selected_month]['Repeating Cst from Last Month']

#---------Past Month--------------
past_sales = data[previous_month]['Revenue']
past_orders = data[previous_month]['Total Orders']
past_cst = data[previous_month]['Total Customers']
past_cst_in_month = data[previous_month]['Total Customers in Month']
past_new_cst = data[previous_month]['New Customers']
past_repeat_cst = data[previous_month]['Repeating Customers']
past_retention_rate = data[previous_month]['Overall Ret.Rate']
past_last_month_rr = data[previous_month]['Ret.Rate wrt. Last Month']
past_repeating_cst_from_last_month = data[previous_month]['Repeating Cst from Last Month']

sales_percent_change = abs(sales - past_sales)/past_sales * 100
sales_percent_change = round(sales_percent_change,2)

orders_change = abs(orders - past_orders)
cst_change = abs(cst - past_cst)
cst_in_month_change = abs(cst_in_month - past_cst_in_month)
rep_cst_change = abs(repeating_cst - past_repeat_cst)
rep_frm_last_month_change = abs(repeating_cst_from_last_month - past_repeating_cst_from_last_month)

r_change = float(retention_rate.replace('%',''))
pr_change = float(past_retention_rate.replace('%',''))
lr_change = float(last_month_rr.replace('%',''))
plr_change = float(past_last_month_rr.replace('%',''))

retention_rate_change = abs(r_change - pr_change)
retention_rate_change = round(retention_rate_change,2)
rr_last_month_change = abs(lr_change - plr_change)
rr_last_month_change = round(rr_last_month_change,2)


def set_divider_vertical(width,height):
    st.markdown(
        f"""
        <div style="display:flex; justify-content:top;">
            <div style="width:{width}px; height:{height}px; background-color:#6E6E6E; margin:auto;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.container():
    st.subheader('Summary Report')

    col1, col_spacer1,col2,col_spacer2, col3,col_spacer3,col4 = st.columns([5,0.5,5,0.5,5,0.5,5])

    with col1:
        st.metric("Total Sales", f"₹{sales}", f"{'+' if sales >= past_sales else '-'}{sales_percent_change}%")

    with col_spacer1:
        set_divider_vertical(2,100)

    with col2:
        st.metric("Total Orders", f"{orders}", f"{'+' if orders >= past_orders else '-'}{orders_change}")
        # st.markdown(f"""
        #   <div style="flex: 1;">
        #     <small>Total Orders</small>
        #     <div style="display: flex; align-items: center; margin-top: -10px">
        #     <p style="margin-right: 5px;  font-size: 35px">{orders}</p>
        #     <p style="font-size: 25px; color: #F5C84D; font-weight: bold">({cst_in_month})</p>
        #     </div>
        #     <div style="display: flex; margin-top: -20px; margin-left: 0px; color: #37BC62; font-weight: bold">
        #         <p style="font-size:25px; margin-top: -10px;margin-right:5px">&#8593;</p>
        #         <p style="font-size:17px">+{orders_change}</p>
        #     </div>
        #   </div>
        # """, unsafe_allow_html=True)

    with col_spacer2:
        set_divider_vertical(2,100)

    with col3:
        st.metric("Total Customers", f"{cst}", f"{'+' if cst >= past_cst else '-'}{cst_change}")

    with col_spacer3:
        set_divider_vertical(2,100)

    with col4:
        st.metric("Total Customers in Month", f"{cst_in_month}", f"{'+' if cst_in_month >= past_cst_in_month else '-'}{cst_in_month_change}")

st.markdown(
            """
            <div style="display:flex; justify-content:top;">
                <div style="width:100%; height:2px; background-color:#6E6E6E; margin: auto";></div>
            </div>
            """,
            unsafe_allow_html=True
        )

with st.container():
    st.subheader('Customers Report')

    col1,col_spacer1, col2,col_spacer2, col3,col_spacer3, col4 = st.columns([5,0.5,5,0.5,5,0.5,5])

    with col1:
        st.metric("Repeating Customers", f"{repeating_cst}", f"{'+' if repeating_cst >= past_repeat_cst else '-'}{rep_cst_change}")

    with col_spacer1:
        set_divider_vertical(2,100)

    with col2:
        st.metric("Retention Rate", f"{retention_rate}", f"{'+' if retention_rate >= past_retention_rate else '-'}{retention_rate_change}%")

    with col_spacer2:
        set_divider_vertical(2,100)

    with col3:
        st.metric("Retention Rate wrt. Last Month", f"{last_month_rr}", f"{'+' if last_month_rr >= past_last_month_rr else '-'}{rr_last_month_change}%")

    with col_spacer3:
        set_divider_vertical(2,100)

    with col4:
        st.metric("Repeating Customers from Last Month", f"{repeating_cst_from_last_month}", f"{'+' if repeating_cst_from_last_month >= past_repeating_cst_from_last_month else '-'}{rep_frm_last_month_change}")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
            """
            <div style="display:flex; justify-content:top;">
                <div style="width:100%; height:2px; background-color:#6E6E6E; margin-top: -60px"></div>
            </div>
            """,
            unsafe_allow_html=True
        )


#------Graph Data-------
week_data = data[selected_month]['Weeks']
df_week = pd.DataFrame(list(week_data.items()),columns=['Week','Revenue'])

day_data = data[selected_month]['Days']
df_day = pd.DataFrame(list(day_data.items()),columns=['Day','Revenue'])
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

if selected_format == 'Weekly Data':
    selected_data = df_week
    x_axis = 'Week'
elif selected_format == 'Daily Data':
    selected_data = df_day
    x_axis = 'Day'
#By Default Weekly Data
else:
    selected_data = df_week
    x_axis = 'Week'


#---------Customers Graph----------
try:
    new_xls = pd.ExcelFile("Spreadsheets/New_Customers.xlsx")
    rep_xls = pd.ExcelFile("Spreadsheets/Repeating_Customers.xlsx")
    rep_lm_xls = pd.ExcelFile("Spreadsheets/Rep_LastMonth_Customers.xlsx")

    # Initialize fallback DataFrames
    new_data = rep_data = rep_lm_data = pd.DataFrame()
    # Read sheets only if they exist
    if selected_month in new_xls.sheet_names:
        new_data = pd.read_excel(new_xls, sheet_name=selected_month)
    if selected_month in rep_xls.sheet_names:
        rep_data = pd.read_excel(rep_xls, sheet_name=selected_month)
    if selected_month in rep_lm_xls.sheet_names:
        rep_lm_data = pd.read_excel(rep_lm_xls, sheet_name=selected_month)

    if x_axis == 'Week':
        new_cst_df = new_data.groupby("Week").size().reset_index(name='Count').set_index('Week')
        rep_cst_df = rep_data.groupby("Week").size().reset_index(name='Count').set_index('Week')
        rep_cst_lm_df = rep_lm_data.groupby("Week").size().reset_index(name='Count').set_index('Week')

    else:
        new_cst_df = new_data.groupby("Day").size().reset_index(name='Count').set_index('Day')
        rep_cst_df = rep_data.groupby("Day").size().reset_index(name='Count').set_index('Day')
        rep_cst_lm_df = rep_lm_data.groupby("Day").size().reset_index(name='Count').set_index('Day')

except Exception as e:
    new_cst_df = pd.DataFrame({'Count': []})
    rep_cst_df = pd.DataFrame({'Count': []})
    rep_cst_lm_df = pd.DataFrame({'Count': []})

data_options = {
    "New Customers": new_cst_df.rename(columns={'Count': 'New Customers'}),
    "Repeating Customers": rep_cst_df.rename(columns={'Count': 'Repeating Customers'}),
    "Repeat from Last Month": rep_cst_lm_df.rename(columns={'Count': 'Repeat from Last Month'})
}

sidebar.subheader('Filter Customer Type')
selected = st.sidebar.multiselect(
    "Select customer types(for chart):",
    options=list(data_options.keys()),
    default=list(data_options.keys())  # All selected by default
)


with st.container():
    col1,col_spacer,col2 = st.columns([5,0.5,5])

    with col1:
        chart = alt.Chart(selected_data).mark_bar().encode(
            x=alt.X(x_axis,sort=day_order),
            y='Revenue',
        ).properties(height=600)
        st.altair_chart(chart,use_container_width=True)
        # st.bar_chart(selected_data,x=x_axis,y="Revenue",width=50,height=600,)

    with col_spacer:
        st.markdown(
            """
            <div style="display:flex; justify-content:top;">
                <div style="width:2px; height:550px; background-color:#6E6E6E; margin:auto;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        if selected:
            # Concatenate only selected columns
            combined_df = pd.concat([data_options[sel] for sel in selected], axis=1)

            if len(combined_df) <= 0:
                st.warning('No data available for for this month.')
            else:
                # Show line chart
                st.line_chart(combined_df,height=600,use_container_width=True,x_label=x_axis,y_label='Count')
        else:
            st.warning("Please select at least one customer type to display the chart.")