('STMT_LIST', [['STMT', 'STMT_LIST'], ['epsilon']])
('RTN_STMT', [['return', 'EXPR']])
('TERM', [['FACTOR', 'TERM2']])
('CODE_BLOCK', [['{', 'STMT_LIST', '}']])
('CMPL_UNIT', [['FUNC_LIST']])
('TERM2', [['*', 'FACTOR', 'TERM2'], ['/', 'FACTOR', 'TERM2'], ['epsilon']])
('FUNC_DEF', [['TYPE_SPEC', 'ID', '(', 'ARG_LIST', ')', 'CODE_BLOCK']])
('CALL_STMT', [['ID', '(', 'ARG_LIST', ')']])
('EXPR', [['TERM', 'EXPR2']])
('ARGUMENT', [['TYPE_SPEC', 'ID']])
('STMT', [['RTN_STMT'], ['ASSIGN_STMT'], ['ITER_STMT'], ['SLCT_STMT'], ['CMP_STMT'], ['CALL_STMT']])
('ASSIGN_STMT', [['ID', '=', 'EXPR']])
('EXPR2', [['+', 'TERM', 'EXPR2'], ['-', 'TERM', 'EXPR2'], ['epsilon']])
('SLCT_STMT', [['if', '(', 'STMT', ')', 'CODE_BLOCK'], ['if', '(', 'STMT', ')', 'STMT']])
('TYPE_SPEC', [['int'], ['void'], ['char'], ['float'], ['double']])
('FACTOR', [['ID'], ['CONST'], ['(', 'EXPR', ')']])
('FUNC_LIST', [['FUNC_DEF', 'FUNC_LIST'], ['epsilon']])
('DECL_STMT', [['TYPE_SPEC', 'ID'], ['TYPE_SPEC', 'ID', '=', 'EXPR']])
('CMP_STMT', [['EXPR', '>', 'EXPR'], ['EXPR', '<', 'EXPR'], ['EXPR', '>=', 'EXPR'], ['EXPR', '<=', 'EXPR'], ['EXPR', '==', 'EXPR'], ['EXPR', '!=', 'EXPR']])
('ITER_STMT', [['for', '(', 'STMT', ';', 'STMT', ';', 'STMT', ')', 'CODE_BLOCK'], ['for', '(', 'STMT', ';', 'STMT', ';', 'STMT', ')', 'STMT']])
('ARG_LIST', [['ARGUMENT'], ['ARGUMENT', ',', 'ARG_LIST'], ['epsilon']])

