module Parser where

import Data.Char
import CinchTypes

-- TODO: Write Parser monad

parse :: [String] -> Maybe Ast
parse tokens = case parseStatementList tokens of
  Just (ast, _) -> Just ast
  Nothing -> Nothing

parseStatementList :: [String] -> Maybe (Ast, [String])
parseStatementList tokens = case parseStatementListHelper [] tokens of
  Nothing -> Nothing
  Just (sl, others) -> Just (Ast { typ=StatementList, name="", children=sl }, others)

parseStatementListHelper :: [Ast] -> [String] -> Maybe ([Ast], [String])
parseStatementListHelper asts [] = Just (reverse asts, [])
parseStatementListHelper asts ("}":tokens) = Just (reverse asts, tokens)
parseStatementListHelper asts tokens = case parseStatement tokens of
  Nothing -> Nothing
  Just (ast, rest) -> parseStatementListHelper (ast:asts) rest



parseExpressionList :: [String] -> Maybe (Ast, [String])
parseExpressionList tokens = case parseExpressionListHelper [] tokens of
  Nothing -> Nothing
  Just (sl, others) -> Just (Ast { typ=ExpressionList, name="", children=sl }, others)

parseExpressionListHelper :: [Ast] -> [String] -> Maybe ([Ast], [String])
parseExpressionListHelper asts [] = Just (reverse asts, [])
parseExpressionListHelper asts (")":tokens) = Just (reverse asts, tokens)
parseExpressionListHelper asts tokens = case parseExpression tokens of
  Nothing -> Nothing
  Just (ast, rest) -> parseExpressionListHelper (ast:asts) rest



parseStatement :: [String] -> Maybe (Ast, [String])
parseStatement ("if":"(":tokens) = parseIfStatement tokens
parseStatement ("while":"(":tokens) = parseWhileLoop tokens
parseStatement ("function":tokens) = parseFuncDef tokens
parseStatement ("return":tokens) = parseReturnStatement tokens
parseStatement (variable:"=":tokens) = parseAssignment (variable:"=":tokens)
parseStatement tokens = parseExpression tokens

parseAssignment :: [String]  -> Maybe (Ast, [String])
parseAssignment tokens = case parseIdentifier tokens of
  Nothing -> Nothing
  Just (name, "=":rest) -> case parseExpression rest of
    Nothing -> Nothing
    Just (expr, others) -> Just (Ast { typ=AssignmentStatement, name="", children=[name, expr] }, others)
  otherwise -> Nothing

parseIfStatement :: [String] -> Maybe (Ast, [String])
parseIfStatement tks = case parseExpression tks of
  Nothing -> Nothing
  Just (cond, ")":body) -> case parseBlock body of
    Nothing -> Nothing
    Just (body, rest) -> Just (Ast { typ=If, name="", children=[cond, body] }, rest)

parseWhileLoop :: [String] -> Maybe (Ast, [String])
parseWhileLoop tks = case parseExpression tks of
  Nothing -> Nothing
  Just (cond, ")":body) -> case parseBlock body of
    Nothing -> Nothing
    Just (body, rest) -> Just (Ast { typ=While, name="", children=[cond, body] }, rest)

parseFuncDef :: [String] -> Maybe (Ast, [String])
parseFuncDef (name:"(":tokens) = case parseIdentifierList tokens of
  Nothing -> Nothing
  Just (argumentNames, newtoks) -> case parseBlock newtoks of
    Nothing -> Nothing
    Just (body, newertoks) -> Just (Ast { typ=FunctionDef, name=name, children=argumentNames++[body] }, newertoks)
parseFuncDef otherwise = Nothing

parseReturnStatement :: [String] -> Maybe (Ast, [String])
parseReturnStatement rest = case parseExpression rest of
  Nothing -> Nothing
  Just (expr, others) -> Just (Ast { typ=Return, name="", children=[expr] }, others)

parseExpression :: [String] -> Maybe (Ast, [String])
parseExpression tokens = case parseExpressionHelper tokens of
  Nothing -> Nothing
  Just (first, []) -> Just (first, [])
  Just (first, op:rest) -> if op `elem` operators then
      parseBinaryExpression first (op:rest)
    else
      Just (first, op:rest)

parseExpressionHelper :: [String] -> Maybe (Ast, [String])
parseExpressionHelper (f:"(":tokens) = parseFuncCall (f:"(":tokens)
parseExpressionHelper tokens
  | all isDigit $ head tokens = parseNumber tokens
  | all isAlpha $ head tokens = parseIdentifier tokens
  | otherwise = Nothing

parseIdentifierList :: [String] -> Maybe ([Ast], [String])
parseIdentifierList = parseIdentifierListHelper []

parseIdentifierListHelper :: [Ast] -> [String] -> Maybe ([Ast], [String])
parseIdentifierListHelper asts (")":rest) = Just (reverse asts, rest)
parseIdentifierListHelper asts tokens = case parseIdentifier tokens of
  Nothing -> Nothing
  Just (ast, rest) -> parseIdentifierListHelper (ast:asts) rest

parseFuncCall :: [String] ->  Maybe (Ast, [String])
parseFuncCall tokens = case parseIdentifier tokens of
  Nothing -> Nothing
  Just (name, "(":rest) -> case parseExpressionList rest of
    Nothing -> Nothing
    Just (args, others) -> Just (
      Ast { typ=FunctionCall, name="", children=[name, args] },
      others)
  otherwise -> Nothing

parseNumber :: [String] ->  Maybe (Ast, [String])
parseNumber (name:tokens) = Just (Ast { typ=IntegerLiteral, name=name, children=[] }, tokens)

parseIdentifier :: [String] -> Maybe (Ast, [String])
parseIdentifier (name:tokens) = Just (Ast { typ=Identifier, name=name, children=[] }, tokens)

parseBinaryExpression :: Ast -> [String] -> Maybe (Ast, [String])
parseBinaryExpression left (operator:tokens) = case parseExpression tokens of
  Nothing -> Nothing
  Just (right, rest) -> Just (Ast { typ=BinaryExpression, name=operator, children=[left, right] }, rest)

parseBlock :: [String] -> Maybe (Ast, [String])
parseBlock ("{":body) = case parseStatementList body of
  Nothing -> Nothing
  Just (ast, rest) -> Just (ast, rest)
parseBlock otherwise = Nothing
