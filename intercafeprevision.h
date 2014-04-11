#ifndef INTERCAFEPREVISION_H
#define INTERCAFEPREVISION_H

#include <QWidget>

namespace Ui {
class intercafePrevision;
}

class intercafePrevision : public QWidget
{
    Q_OBJECT

public:
    explicit intercafePrevision(QWidget *parent = 0);
    ~intercafePrevision();

private:
    Ui::intercafePrevision *ui;
};

#endif // INTERCAFEPREVISION_H
