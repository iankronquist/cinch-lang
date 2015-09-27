module Parser where

import Data.Char
import CinchTypes

-- TODO: Write Parser monad
-- FIXME: Check that tokens like "(" and "{" are what we think and don't just 
-- ignore them

parse :: [String] -> Ast
parse tokens = do
  let (ast, _) = parse_statement_list tokens
  ast


parse_statement_list :: [String] -> (Ast, [String])
parse_statement_list tokens = do
  let (sl, others) = parse_statement_list_helper [] tokens
  (Ast { typ=StatementList, name="", children=sl }, others)

parse_statement_list_helper :: [Ast] -> [String] -> ([Ast], [String])
parse_statement_list_helper asts [] = (asts, [])
parse_statement_list_helper asts tokens = do
  let (ast, rest) = parse_statement tokens
  parse_statement_list_helper (asts++[ast]) rest


parse_statement :: [String] -> (Ast, [String])
parse_statement ("if":tokens) = parse_if_statement tokens
parse_statement ("while":tokens) = parse_while_loop tokens
parse_statement ("function":tokens) = parse_while_loop tokens
parse_statement ("return":tokens) = parse_while_loop tokens
parse_statement tokens = parse_expression tokens

parse_assignment :: [String]  -> (Ast, [String])
parse_assignment tokens = do
  let (name, rest) = parse_identifier tokens
  let (expr, others) = parse_expression $ tail rest
  (Ast { typ=AssignmentStatement, name="", children=[name, expr] }, others)

parse_if_statement :: [String] -> (Ast, [String])
parse_if_statement ("if":"(":tks) = do
  let (cond, bodytks) = parse_expression tks
  let (body, rest) = parse_block $ tail bodytks
  (Ast { typ=If, name="", children=[cond, body] }, rest)

parse_while_loop :: [String] -> (Ast, [String])
parse_while_loop ("while":"(":tks) = do
  let (cond, bodytks) = parse_expression tks
  let (body, rest) = parse_block $ tail bodytks
  (Ast { typ=If, name="", children=[cond, body] }, rest)

parse_func_def :: [String] -> (Ast, [String])
parse_func_def ("function":tokens) = do
  let name = head tokens
  let (argument_names, newtoks) = parse_identifier_list $ tail $ tail tokens
  let (body, newertoks) = parse_block $ tail newtoks
  (Ast { typ=FunctionDef, name=name, children=argument_names++[body] }, newertoks)

parse_return_statement :: [String] -> (Ast, [String])
parse_return_statement ("return":rest) = do
  let (expr, others) = parse_expression rest
  (Ast { typ=Return, name="", children=[expr] }, others)

parse_expression :: [String] -> (Ast, [String])
parse_expression tokens = do
  let (first, rest) = parse_expression_helper tokens
  if (length rest > 0) && (head rest `elem` operators) then parse_binary_expression first rest else (first, rest)

parse_expression_helper :: [String] -> (Ast, [String])
parse_expression_helper (f:"(":tokens) = parse_func_call (f:"(":tokens)
parse_expression_helper tokens
  | all isDigit $ head tokens = parse_number tokens
  | otherwise = parse_identifier tokens

parse_identifier_list :: [String] -> ([Ast], [String])
parse_identifier_list tokens = parse_identifier_list_helper [] tokens

parse_identifier_list_helper :: [Ast] -> [String] -> ([Ast], [String])
parse_identifier_list_helper asts (")":rest) = (reverse asts, rest)
parse_identifier_list_helper asts tokens = do
  let (ast, rest) = parse_identifier tokens
  (parse_identifier_list_helper (ast:asts) rest)

parse_func_call :: [String] ->  (Ast, [String])
parse_func_call tokens = do
  let (name, rest) = parse_identifier tokens
  let (args, others) = parse_identifier_list $ tail rest
  (Ast { typ=FunctionCall, name="", children=name:args }, tail others)

parse_number :: [String] ->  (Ast, [String])
parse_number tokens = (Ast { typ=IntegerLiteral, name=head tokens, children=[] }, tail tokens)

parse_identifier :: [String] -> (Ast, [String])
parse_identifier tokens = (Ast { typ=Identifier, name=tokens !! 0, children=[] }, tail tokens)

parse_binary_expression :: Ast -> [String] -> (Ast, [String])
parse_binary_expression left tokens = do
  let foo = tail []
  let operator = head tokens
  let (right, rest) = parse_expression $ tail tokens
  (Ast { typ=BinaryExpression, name=operator, children=[right] }, rest)

parse_block :: [String] -> (Ast, [String])
parse_block ("{":body) = do
  let (ast, rest) = parse_statement_list body
  (ast, tail rest)
