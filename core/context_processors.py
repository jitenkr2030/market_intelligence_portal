from .modules import MODULES
def module_menu(request): return {"module_menu":list(MODULES.items())}
