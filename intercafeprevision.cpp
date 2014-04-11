#include "intercafeprevision.h"
#include "ui_intercafeprevision.h"

intercafePrevision::intercafePrevision(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::intercafePrevision)
{
    ui->setupUi(this);
}

intercafePrevision::~intercafePrevision()
{
    delete ui;
}
