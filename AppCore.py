from GraphEngine import GraphEngine
from WeightNormalizer import WeightNormalizer
from Recommendation import Recommendation  
from UIDisplay import UIDisplay 


class AppCore:
    def __init__(self):
        self.normalizer = WeightNormalizer()
        self.graph_engine = GraphEngine(self.normalizer)
        self.recommender = None
        self.ui = UIDisplay()

    def run(self, user_interactions: dict, login_user: str):
        # user_interactions
        graph = self.graph_engine.build_graph(user_interactions)
        self.recommender = Recommendation(graph)

        results = self.recommender.weighted_bfs(login_user)

        self.ui.show_recommendations(login_user, results)