#! /usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import sys, csv, os

class EngineBox( QComboBox ):
	def __init__( self, enginePath, parent = None ):
		QComboBox.__init__( self, parent )

		fi = QFileInfo( qApp.arguments()[0] )
		if fi.isSymLink():
			fi = QFileInfo( fi.symLinkTarget() )
		self.PATH = os.path.join( unicode( fi.absolutePath() ), enginePath )

		self.load()

	def load( self ):
		self.clear()
		fin = csv.reader( open( self.PATH ) )
		for line in fin:
			self.addItem( line[0], QVariant( line[1] ) )

	def getCurrent( self ):
		return self.itemData( self.currentIndex() ).toString()

class MainWindow( QMainWindow ):
	def __init__( self, parent = None ):
		QMainWindow.__init__( self, parent )

		self.__initToolBar()

		self.center = QWebView( self )
		self.setCentralWidget( self.center )
		self.center.load( QUrl( 'about:blank' ) )

		self.__initStatusBar()

	def __initToolBar( self ):
		toolBar = QToolBar( self )
		self.addToolBar( toolBar )
		toolBar.setMovable( False )

		self.uri = QLineEdit( self )
		toolBar.addWidget( self.uri )
		self.connect( self.uri, SIGNAL( 'returnPressed()' ), self.load )

		toolBar.addSeparator()

		self.engines = EngineBox( 'engines.csv', self )
		toolBar.addWidget( self.engines )

		reload_ = QPushButton( 'Reload', self )
		toolBar.addWidget( reload_ )
		self.connect( reload_, SIGNAL( 'clicked()' ), self.engines.load )

	def __initStatusBar( self ):
		status = QStatusBar( self )
		self.setStatusBar( status )
		progress = QProgressBar( status )
		status.addWidget( progress )
		progress.hide()
		status.showMessage( 'Ready' )

		self.connect( self.center, SIGNAL( 'loadStarted()' ), progress, SLOT( 'show()' ) )
		self.connect( self.center, SIGNAL( 'loadProgress( int )' ), progress, SLOT( 'setValue( int )' ) )
		self.connect( self.center, SIGNAL( 'loadFinished( bool )' ), lambda ok: ok and progress.hide() )

	def load( self ):
		self.center.load( QUrl( self.engines.getCurrent().arg( self.uri.text() ) ) )

def main( args = None ):
	if args is None:
		args = sys.argv

	app = QApplication( args )

	window = MainWindow()
	window.setWindowTitle( 'QuePy' )
	window.resize( 800, 600 )
	window.show()

	return app.exec_()

if __name__ == '__main__':
	sys.exit( main() )