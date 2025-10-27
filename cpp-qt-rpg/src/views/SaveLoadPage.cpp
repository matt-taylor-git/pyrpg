#include "SaveLoadPage.h"
#include "../theme/Theme.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QListWidget>
#include <QPushButton>
#include <QFrame>
#include <QFileDialog>

SaveLoadPage::SaveLoadPage(QWidget *parent) : QWidget(parent)
{
    setupUi();
}

void SaveLoadPage::setupUi()
{
    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG, Theme::SPACING_LG);
    mainLayout->setSpacing(Theme::SPACING_LG);

    QLabel *title = new QLabel("💾 Save & Load Game");
    title->setStyleSheet("font-size: 24px; font-weight: bold;");
    mainLayout->addWidget(title, 0, Qt::AlignCenter);

    QHBoxLayout *contentLayout = new QHBoxLayout();
    contentLayout->setSpacing(Theme::SPACING_LG);

    // Left side: Saves list
    QFrame *savesSection = new QFrame();
    QVBoxLayout *savesLayout = new QVBoxLayout(savesSection);
    m_savesList = new QListWidget();
    m_savesList->addItem("Save Slot 1 (Placeholder)");
    savesLayout->addWidget(new QLabel("📁 Save Files"));
    savesLayout->addWidget(m_savesList);
    m_deleteButton = new QPushButton("🗑️ Delete");
    savesLayout->addWidget(m_deleteButton);
    contentLayout->addWidget(savesSection);

    // Right side: Actions
    QFrame *actionsSection = new QFrame();
    QVBoxLayout *actionsLayout = new QVBoxLayout(actionsSection);
    m_quickSaveButton = new QPushButton("⚡ Quick Save");
    m_quickLoadButton = new QPushButton("⚡ Quick Load");
    m_saveSelectedButton = new QPushButton("💾 Save Over Selection");
    m_loadSelectedButton = new QPushButton("📁 Load Selection");
    m_newSaveButton = new QPushButton("🆕 New Save Slot");
    actionsLayout->addWidget(new QLabel("🎮 Game Actions"));
    actionsLayout->addWidget(m_quickSaveButton);
    actionsLayout->addWidget(m_quickLoadButton);
    actionsLayout->addWidget(m_saveSelectedButton);
    actionsLayout->addWidget(m_loadSelectedButton);
    actionsLayout->addWidget(m_newSaveButton);
    contentLayout->addWidget(actionsSection);

    mainLayout->addLayout(contentLayout);

    // Connect buttons
    connect(m_quickSaveButton, &QPushButton::clicked, this, &SaveLoadPage::onQuickSaveClicked);
    connect(m_quickLoadButton, &QPushButton::clicked, this, &SaveLoadPage::onQuickLoadClicked);
    connect(m_saveSelectedButton, &QPushButton::clicked, this, &SaveLoadPage::onSaveSelectedClicked);
    connect(m_loadSelectedButton, &QPushButton::clicked, this, &SaveLoadPage::onLoadSelectedClicked);
    connect(m_newSaveButton, &QPushButton::clicked, this, &SaveLoadPage::onNewSaveClicked);
}

void SaveLoadPage::onQuickSaveClicked()
{
    emit quickSaveRequested();
}

void SaveLoadPage::onQuickLoadClicked()
{
    emit quickLoadRequested();
}

void SaveLoadPage::onSaveSelectedClicked()
{
    QString filePath = QFileDialog::getSaveFileName(this, "Save Game", "", "Game Save Files (*.dat)");
    if (!filePath.isEmpty()) {
        emit saveToFileRequested(filePath);
    }
}

void SaveLoadPage::onLoadSelectedClicked()
{
    QString filePath = QFileDialog::getOpenFileName(this, "Load Game", "", "Game Save Files (*.dat)");
    if (!filePath.isEmpty()) {
        emit loadFromFileRequested(filePath);
    }
}

void SaveLoadPage::onNewSaveClicked()
{
    emit newSaveRequested();
}