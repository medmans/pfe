#ifndef CHARGEPERSONNEL_H
#define CHARGEPERSONNEL_H

#include <QWidget>

namespace Ui {
class chargePersonnel;
}

class chargePersonnel : public QWidget
{
    Q_OBJECT

public:
    explicit chargePersonnel(QWidget *parent = 0);
    ~chargePersonnel();

private:
    Ui::chargePersonnel *ui;
};

#endif // CHARGEPERSONNEL_H
