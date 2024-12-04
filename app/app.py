# Import necessary libraries
import seaborn as sns  # Seaborn for visualizations (though not used in this version)
import plotly.express as px  # Plotly for interactive charts
from faicons import icon_svg  # For icons in the UI
from shiny import reactive  # For reactivity in Shiny
from shiny.express import input, render, ui  # For UI, input, and render components
import palmerpenguins  # Dataset containing information about penguins

# Load the penguin dataset
df = palmerpenguins.load_penguins()

# Set up the page options, including title and the ability to fill the page
ui.page_opts(title="Palmer Penguins dashboard", fillable=True)

# Sidebar with filter controls
with ui.sidebar(title="Filter controls"):
    # Slider to filter by mass (weight of penguins)
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    
    # Checkbox group to filter by species (Adelie, Gentoo, Chinstrap)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selection
    )
    
    ui.hr()  # Horizontal line for separation
    ui.h6("Links")  # Section for external links
    
    # External links related to the app, source code, issues, etc.
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main content layout, using column wrap for responsiveness
with ui.layout_column_wrap(fill=False):
    # Box to display the number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"
        
        @render.text
        def count():
            # Return the count of filtered penguins
            return filtered_df().shape[0]

    # Box to display average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"
        
        @render.text
        def bill_length():
            # Return the average bill length of filtered penguins
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Box to display average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"
        
        @render.text
        def bill_depth():
            # Return the average bill depth of filtered penguins
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout for the two cards: one for the scatter plot and one for the data table
with ui.layout_columns():
    # Card for displaying the interactive Plotly scatter plot
    with ui.card(full_screen=True):
        ui.card_header("Bill length vs Depth")
        
        @render.ui
        def length_depth():
            # Create an interactive Plotly scatter plot
            fig = px.scatter(
                filtered_df(),  # Use the filtered dataset
                x="bill_length_mm",  # X-axis is bill length
                y="bill_depth_mm",  # Y-axis is bill depth
                color="species",  # Color points by species
                title="Bill Length vs Depth",  # Title of the plot
                labels={"bill_length_mm": "Bill Length (mm)", "bill_depth_mm": "Bill Depth (mm)"},  # Axis labels
            )
            # Convert the Plotly figure to HTML for embedding in the UI
            return ui.HTML(fig.to_html(full_html=False))

    # Card for displaying the filtered data in a table format
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")
        
        @render.data_frame
        def summary_statistics():
            # Select relevant columns to display in the data grid
            cols = [
                "species",  # Species of the penguin
                "island",  # Island where the penguin was found
                "bill_length_mm",  # Bill length in mm
                "bill_depth_mm",  # Bill depth in mm
                "body_mass_g",  # Body mass in grams
            ]
            # Return the filtered data for the selected columns
            return render.DataGrid(filtered_df()[cols], filters=True)

# Calculate the filtered data based on user inputs
@reactive.calc
def filtered_df():
    # Filter by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Filter by selected mass range
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df  # Return the filtered DataFrame
