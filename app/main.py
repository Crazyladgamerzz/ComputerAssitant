if __name__ == '__main__':
    from GRAPH import config
    from GRAPH.main_graph import MainGraph
    from GRAPH.llms import LLMModels,LLMModel
    from menu import Menu,MenuAction
    import os
    from dotenv import load_dotenv

    #Developer configurations
    config.DEBUG_GRAPH = True
    config.CONFIRM_EVERY_LOOP = True
    config.SKIP_SECURITY = True

    #Backend config
    config.MAX_SCRATCHPAD_LEN = 2000 #tokens

    menu = Menu()

    if not load_dotenv(os.path.join(os.path.dirname(__file__),'.env')):
        menu.request_enter(msg='Failed to load envirnoment variables.')

    def get_main_graph():
        config.load_config()
        llm_models = LLMModels(agent_llm_model=LLMModel.default(LLMModel.Defaults.GPT_OSS120b,reasoning='low',temperature=0.6),
                            scratchpad_llm_model=LLMModel.default(LLMModel.Defaults.LLAMA3b,temperature=0.2),
                            security_llm_model=LLMModel.default(LLMModel.Defaults.LLAMA3b,temperature=0.1))
        return MainGraph(llm_models=llm_models,
                        human_validation=config.config.EXEC_HUMAN_CONFIRMATION,
                        max_iterations=config.config.MAX_ITERATIONS)

    main_graph = get_main_graph()

    while(menu.is_running):
        action,user_input = menu.display_menu()

        if action == MenuAction.REQUEST_AGENT_ACTION:
            response = main_graph.invoke(user_input=user_input)
            menu.request_enter(msg=response['final_answer'])
        elif action == MenuAction.SET_HUMAN_CONFIRMATION_ACTION:
            menu.request_enter(msg= config.config.set_human_confirmation(b=user_input) )
            main_graph = get_main_graph()
        elif action == MenuAction.SET_MAXITERATIONS_ACTION:
            menu.request_enter(msg= config.config.set_max_iterations(max_iterations=user_input))
            main_graph = get_main_graph()


