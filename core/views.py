from django.shortcuts import render
from core.telegram_parser import parser_telegram



def show_posts(self):
    parser_telegram()
    return self