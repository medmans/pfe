#include "chargepersonnel.h"
#include "ui_chargepersonnel.h"

chargePersonnel::chargePersonnel(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::chargePersonnel)
{
    ui->setupUi(this);
}

chargePersonnel::~chargePersonnel()
{
    delete ui;
}
