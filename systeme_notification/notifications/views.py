# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .core import Epidemie, Incendie, Innondation, Securite

# class EvacuationViewSet(viewsets.ViewSet):
#     """
#     Centralized ViewSet handling all evacuation types (epidemie, incendie, etc.)
#     """

#     # GET /api/evacuation/epidemie/
#     @action(detail=False, methods=["get"])
#     def epidemie(self, request):
#         return Response({"message": "Évacuation Épidémie prête à être déclenchée"})

#     # POST /api/evacuation/epidemie/
#     @action(detail=False, methods=["post"])
#     def epidemie(self, request):
#         e = Epidemie()
#         e.evacuer()
#         return Response({"status": "Évacuation Épidémie déclenchée"})

#     # GET /api/evacuation/incendie/
#     @action(detail=False, methods=["get"])
#     def incendie(self, request):
#         return Response({"message": "Évacuation Incendie prête à être déclenchée"})

#     # POST /api/evacuation/incendie/
#     @action(detail=False, methods=["post"])
#     def incendie(self, request):
#         i = Incendie()
#         i.evacuer()
#         return Response({"status": "Évacuation Incendie déclenchée"})

#     # GET /api/evacuation/innondation/
#     @action(detail=False, methods=["get"])
#     def innondation(self, request):
#         return Response({"message": "Évacuation Inondation prête à être déclenchée"})

#     # POST /api/evacuation/innondation/
#     @action(detail=False, methods=["post"])
#     def innondation(self, request):
#         n = Innondation()
#         n.evacuer()
#         return Response({"status": "Évacuation Inondation déclenchée"})

#     # GET /api/evacuation/securite/
#     @action(detail=False, methods=["get"])
#     def securite(self, request):
#         return Response({"message": "Évacuation Sécurité prête à être déclenchée"})

#     # POST /api/evacuation/securite/
#     @action(detail=False, methods=["post"])
#     def securite(self, request):
#         s = Securite()
#         s.evacuer()
#         return Response({"status": "Évacuation Sécurité déclenchée"})
