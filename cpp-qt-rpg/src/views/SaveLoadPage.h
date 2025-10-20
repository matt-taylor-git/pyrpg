#ifndef SAVELOADPAGE_H
#define SAVELOADPAGE_H

#include <QWidget>

class QListWidget;
class QPushButton;

class SaveLoadPage : public QWidget
{
    Q_OBJECT
public:
    explicit SaveLoadPage(QWidget *parent = nullptr);

signals:
    void quickSaveRequested();
    void quickLoadRequested();
    void saveToFileRequested(const QString &filePath);
    void loadFromFileRequested(const QString &filePath);
    void newSaveRequested();

private slots:
    void onQuickSaveClicked();
    void onQuickLoadClicked();
    void onSaveSelectedClicked();
    void onLoadSelectedClicked();
    void onNewSaveClicked();

private:
    void setupUi();

    QListWidget *m_savesList;
    QPushButton *m_deleteButton;
    QPushButton *m_quickSaveButton;
    QPushButton *m_quickLoadButton;
    QPushButton *m_saveSelectedButton;
    QPushButton *m_loadSelectedButton;
    QPushButton *m_newSaveButton;
};

#endif // SAVELOADPAGE_H