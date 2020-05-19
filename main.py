from app import app, model_div, exploration_div
from data_exploration import html_elements as exploration_html
from prediction_model import html_elements as model_html
from model_visualization import model_visualization_html

if __name__ == '__main__':
    model_div.children = model_html + model_visualization_html
    exploration_div.children = exploration_html
    app.run_server(debug=True, use_reloader=False)
