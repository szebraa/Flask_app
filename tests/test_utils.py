import pytest, os

class Test_utils:

    def test_remove_file(self,utils):
        expected = False
        file = '/tmp/testfile.txt'
        open(file,'a').close()
        utils.remove_file(file)
        result = os.path.exists(file)
        assert expected == result

    def test_reset_sums(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,0,0]
        current_app.config['grossRevenue'] = 9123 
        current_app.config['expenses'] = 10
        current_app.config['netRevenue'] = -123
        utils.reset_sums()
        res = [current_app.config.get('grossRevenue',0),current_app.config.get('expenses',0), current_app.config.get('expenses',0)]
        assert res == expected
    
    def test_reset_entries_counter(self,app,current_app,utils):
        app.app_context().push()
        expected = [0,False]
        current_app.config['entries'] = 9111 
        current_app.config['calculated'] = True
        utils.reset_entries_counter()
        res = [current_app.config.get('entries',0), current_app.config.get('calculated',0)]
        assert res == expected