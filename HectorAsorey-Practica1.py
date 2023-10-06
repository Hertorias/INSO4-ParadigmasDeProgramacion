from sched import scheduler
from time import sleep
import tkinter as tk
from tkinter import ttk
import asyncio
from turtle import numinput
from urllib.request import urlopen
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import io
from rx import create
from rx.core import Observer
from rx.scheduler.eventloop import AsyncIOScheduler
import rx.operators as ops
import rx

#Paginas con las que he probado:
#https://www.amazon.es/Mini-Helmet-Miniatura-colecci%C3%B3n-4100153/dp/B0B7CMPTVR/ref=sr_1_3?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=220Q80F4UAQKW&keywords=fernando+alonso&qid=1671657245&sprefix=fernando+alonso%2Caps%2C92&sr=8-3
#https://store.playstation.com/es-es/product/EP9000-CUSA34388_00-GOWRAGNAROK00000
#https://www.halowaypoint.com/news/autumn-archives

class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()

class Window(tk.Tk):

    def __init__(self, loop):
        self.listaImages = []
        self.contador = 0
        self.errores = 0
        self.numImagenes = 0
        self.linkImagen = ''
        self.imagenActual = ''

        self.loop = loop
        self.root = tk.Tk()
        self.root.title("Practica Paradigmas H. Asorey")
        self.root.geometry('500x380')
        self.label = tk.Label()
        self.text_input = tk.Entry()
        self.lst = tk.Listbox()
        self.text_input.grid(row=0, column=1, columnspan = 2, padx=(8, 8), pady=(16, 0))
        self.labelError = tk.Label(text="")
        self.labelError.grid(row = 1, column=1, columnspan= 2, padx=(8,8), pady=(16,0))
        self.lst.grid(row=2, column = 0, padx=(8, 8), pady=(16, 0))
        self.lst.bind("<<ListboxSelect>>", self.showImage)
        self.label.grid(row=2, column = 1, padx=(8, 8), pady=(16, 0))
        self.progressbar = ttk.Progressbar(length=100)
        self.progressbar.grid(row=3, column=1, columnspan=2, padx=(8, 8), pady=(16, 0))
        self.label2 = tk.Label(text="")
        self.label2.grid(row=4, column=1, columnspan = 2, padx=(8, 8), pady=(16, 0))
        self.label3 = tk.Label(text="")
        self.label3.grid(row=5, column=1, columnspan = 2, padx=(8, 8), pady=(16, 0))
        self.observer = create(self.on_subscribe)
        button_non_block = tk.Button(text="Descargar imagenes", width=16, command=lambda: self.loop.create_task(self.empieza()))
        button_non_block.grid(row=6, column=1, columnspan = 2, padx=(8, 8), pady=(16, 0))

    def actualizaProgressBar(self):
        self.progressbar["value"] = self.contador * 100 / self.numImagenes - 0.1

    def rellenaProgressBar(self):
        self.progressbar["value"] = 99

    def actualizaLista(self, nombre):
        print("Actualizando valores...")
        self.lst.insert(tk.END, nombre)
        self.progressbar["value"] = self.contador * 100 / (self.numImagenes - self.errores) - 0.1

    def showImage(self, e):
        n = self.lst.curselection()

        temp_img = Image.open(io.BytesIO(self.listaImages[n[0]]))
        temp_img = temp_img.resize((160, 120), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(temp_img)
        self.label.config(image=img)
        self.label.image = img
        
    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)

    async def empieza(self):
        self.lst.delete(0, tk.END)
        self.progressbar["value"] = 0
        self.label.config(image='')

        self.numImagenes = 0
        self.errores = 0
        self.contador = 0
        self.listaImages = []
        self.linkImagen = ''
        self.imagenActual = ''

        self.label2.config(text = '')
        self.label3.config(text = '')

        self.observer.subscribe(
            scheduler = AsyncIOScheduler(self.loop),
            on_next = lambda v: self.actualizaLista(v)
        )

    def on_subscribe(self, observer, scheduler):

        async def obtenerImagenes(linkImagen, nombre):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(str(linkImagen)) as resp2:
                        if resp2.status == 200:
                            self.linkImagen = linkImagen
                            self.contador += 1
                            content = await resp2.read()
                            self.listaImages.append(content)
                            self.label2.config(text = f'Se han descargado {self.contador}\nde {self.numImagenes - self.errores} imagenes')
                            #await asyncio.sleep(5)
                            observer.on_next(nombre)
                except aiohttp.InvalidURL:
                    self.errores += 1
                    self.label3.config(text = f'No se han podido obtener todas las imagenes\nNumero de errores: {self.errores}')
                    print("Ruta a la imagen incorrecta")

        async def peticionAPaginaWeb():

            web = self.text_input.get()

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(web) as resp:

                        if resp.status == 200:

                            self.labelError.config(text="")
                            a = await resp.text()

                            listaImagenes = []
                            listaNombres = []

                            soup = BeautifulSoup(a, 'html.parser')
                            for link in soup.find_all('img'):

                                linkImagen = link.get('src')
                                listaImagenes.append(linkImagen)

                                listaNombres.append(link.get('alt'))

                            tareasARealizar = []

                            self.numImagenes = len(listaImagenes)

                            for i in range (len(listaImagenes)):
                                tareasARealizar.append(obtenerImagenes(listaImagenes[i], listaNombres[i]))

                            await asyncio.gather(*tareasARealizar)

                            observer.on_completed()
            except:
                self.labelError.config(text="Introduzca una URL valida")
        self.loop.create_task(peticionAPaginaWeb())
        
asyncio.run(App().exec())