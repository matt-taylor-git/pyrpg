#ifndef NEWGAMEVIEW_H
#define NEWGAMEVIEW_H

#include <QWidget>

class QLabel;
class QLineEdit;
class QPushButton;
class QVBoxLayout;
class QHBoxLayout;
class QFrame;
class QComboBox;
class ValidationLabel; // Forward declaration

class NewGameView : public QWidget
{
    Q_OBJECT
public:
    explicit NewGameView(QWidget *parent = nullptr);

signals:
    void characterCreated(const QString &name, const QString &characterClass);

private slots:
    void validateNameInput();
    void startGame();

private:
    void setupUi();

    QLabel *m_mainTitle;
    QLabel *m_subtitle;
    QFrame *m_createCard;
    QLineEdit *m_nameInput;
    QComboBox *m_classSelector;
    ValidationLabel *m_validationLabel;
    QPushButton *m_startButton;
    QLabel *m_footerLabel;
    QFrame *m_charPreview; // Placeholder for CharacterPreview
};

#endif // NEWGAMEVIEW_H