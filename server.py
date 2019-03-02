import pandas as pd
from flask import *
from sqlalchemy import create_engine
import os

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))


@app.route("/", methods=["GET", "POST"])
def output():
    # These two lines are what really took most of my time. I tried lots complicated options. Then, of course, I RTFM.
    # This redirects when the buttons POSTs.
    if request.method == 'POST':
        return redirect(url_for('run'))
    return render_template('index.html')


@app.route('/run/')
def run():
    df1 = import_csv("example_report.csv.gz")
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/test')
    load_table(df1, engine)
    # Pulling back what I just wrote to the database.
    df2 = pd.read_sql_query('select * from public.dtr', con=engine)
    # print(dir_path)
    # Creating GZIP CSV file of table results
    df2.to_csv(dir_path + '\\results_report.csv.gz', compression='gzip', index=False)
    # print(df2)
    length = len(df2)
    # Render data frame results
    return render_template('view.html', length=length, dataframe=df2.to_html())


def import_csv(file):
    # Load in provided file.
    df = pd.read_csv(file, compression='gzip', header=0, sep=',', quotechar='"')
    # This is what you're probably looking for. Everything else can be looked up or referenced but
    # thinking about the data-- what it is, where it is going and what it might be used for -- is the real check.
    #
    # Convert to timestamp
    df['Day'] = pd.to_datetime(df['Day'], format='%Y-%m-%d', errors='coerce')
    df['Start date'] = pd.to_datetime(df['Start date'], format='%Y-%m-%d', errors='coerce')
    df['End date'] = pd.to_datetime(df['End date'], format='%Y-%m-%d', errors='coerce')
    #
    # Convert percentages to float. For the percentages to be of any application besides a label, they were going
    # need to be converted to a float data type. We could have both but an extra column would be redundant and
    # possibly confusing.
    df['Conv. rate'] = df['Conv. rate'].replace({'%': '', ',': ''}, regex=True)
    df['Conv. rate'] = df['Conv. rate'].astype('float') / 100.0
    df['CTR'] = df['CTR'].str.rstrip('%').astype('float') / 100.0
    df['Search Lost IS (rank)'] = df['Search Lost IS (rank)'].str.rstrip('%').astype('float') / 100.0
    df['Interaction Rate'] = df['Interaction Rate'].str.rstrip('%').astype('float')
    # Convert decimals to float.
    df['Avg. position'] = df['Interaction Rate'].astype('float')
    # The parenthesis in the column name seemed to jam up the table names when I was creating the table. I could have
    # investigated further but I just changed the column name and dropped the original column.
    #
    # While we're on the topic of column names, I normally use all lowercase with underscores when I don't have a house
    # style to follow. Spaces require quotes in queries and some (older?) databases consider capital letters different
    # from lowercase, which can lead to confusion.
    df['Search Lost IS rank'] = df['Search Lost IS (rank)'].astype('float')
    df.drop(['Search Lost IS (rank)'], axis=1, inplace=True)
    # Pandas could use a money data type. I'm converting to float here.
    df['Budget'] = df['Budget'].astype('float') / 100.0
    df['Cost'] = df['Cost'].astype('float') / 100.0
    # Convert IDs to integers. I've got feelings on this. I assume these will likely be indexed. My understanding is
    # that integer keys will lookup faster than strings.
    df['Customer ID'] = df['Customer ID'].astype('int')
    df['Campaign ID'] = df['Campaign ID'].astype('int')
    df['Budget ID'] = df['Budget ID'].astype('int')
    # Convert to integers.
    df['Clicks'] = df['Clicks'].astype('int')
    df['Interactions'] = df['Interactions'].astype('int')
    df['Invalid clicks'] = df['Invalid clicks'].astype('int')
    df['Conversions'] = df['Conversions'].astype('int')
    # Convert to Boolean. Just converting true/false states to Boolean.
    en = {'enabled': True, 'disabled': False}
    df['Campaign state'] = df['Campaign state'].map(en)
    df['Budget explicitly shared'] = df['Budget explicitly shared'].astype('bool')
    # Nulls. I could have set the IDs to NaNs but I didn't know what data type the Label ID was.
    df['Label IDs'] = df['Label IDs'].replace({'--': None}, regex=True)
    df['Labels'] = df['Labels'].replace({'--': None}, regex=True)
    # Convert to category. This is a finite list of text values.
    df['Campaign'] = df['Campaign'].astype('category')
    df['Campaign serving status'] = df['Campaign serving status'].astype('category')
    return df


def load_table(df1, engine):
    # df1.to_sql('test', engine)
    # I cheated a little bit here to save some time. I created the table then selected CREATE TABLE, edited that
    # to the data types I wanted that weren't explicit in pandas (like money) and rebuilt the CREATE TABLE below.
    engine.execute(
        'DROP TABLE IF EXISTS public.dtr;CREATE TABLE public.dtr(index bigint,"Day" timestamp without time zone,'
        '"Customer ID" integer,"Campaign ID" integer,"Campaign" text COLLATE pg_catalog."default","Campaign state" '
        'boolean,"Campaign serving status" text COLLATE pg_catalog."default","Clicks" integer,"Start date" timestamp '
        'without time zone,"End date" timestamp without time zone,"Budget" money,"Budget ID" integer,"Budget explicitly '
        'shared" boolean,"Label IDs" text COLLATE pg_catalog."default","Labels" text COLLATE pg_catalog."default",'
        '"Invalid clicks" integer,"Conversions" integer,"Conv. rate" double precision,"CTR" double precision,"Cost" '
        'money,"Impressions" integer,"Avg. position" double precision,"Interaction Rate" double precision,"Interactions" '
        'integer,"Search Lost IS rank" double precision)WITH (OIDS = FALSE)TABLESPACE pg_default;ALTER TABLE public.dtr '
        'OWNER to postgres;')
    # I left the index in there on purpose
    df1.to_sql("dtr", engine, if_exists='append', chunksize=1000)
    return


if __name__ == "__main__":
    app.run(debug=True)
