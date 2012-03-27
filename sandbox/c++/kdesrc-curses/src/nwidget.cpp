#include "nwidget_p.hpp"
#include "napplication_p.hpp"

#include <algorithm>

NWidget::Private::Private( NWidget * parent ):
children(),
keyPressed(),
parent( parent ),
pos(),
window( NULL ) {
	if( parent == NULL ) {
		this->window = newwin( 0, 0, 0, 0 );
	} else {
		NPoint pos = parent->pos();
		this->window = newwin( 0, 0, pos.y(), pos.x() );
	}
	box( this->window, 0, 0 );
}

NWidget::Private::~Private() {
	std::for_each( std::begin( this->children ), std::end( this->children ), []( NWidget * c ) {
		delete c;
	} );

	delwin( this->window );
}

NWidget::NWidget( NWidget * parent ):
p_( new Private( parent ) ) {
	if( parent != NULL ) {
		parent->p_->children.push_back( this );
	}
	NApplication::instance().p_->addWidget( this );
}

NWidget::~NWidget() {
	NApplication::instance().p_->removeWidget( this );
}

NWidget * NWidget::parent() const {
	return this->p_->parent;
}

const NPoint & NWidget::pos() const {
	return this->p_->pos;
}

// FIXME recreate window here, should be more elegant
void NWidget::resize( int rows, int cols ) {
	NPoint pos = this->pos();
	delwin( this->p_->window );
	this->p_->window = newwin( rows, cols, pos.y(), pos.x() );
	box( this->p_->window, 0, 0 );
	// TODO update children geo
}

void NWidget::update() {
	wrefresh( this->p_->window );
}

boost::signal< void ( int ) > & NWidget::keyPressed() {
	return this->p_->keyPressed;
}

void NWidget::inputEvent( int keyCode ) {
	this->p_->keyPressed( keyCode );
}
