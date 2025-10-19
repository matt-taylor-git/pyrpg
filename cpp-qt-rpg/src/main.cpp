#include <QApplication>
#include "MainWindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // Set application details
    app.setApplicationName("Pyrpg-Qt");
    app.setOrganizationName("Gemini");
    app.setApplicationVersion("1.0");

    MainWindow window;
    window.show();

    return app.exec();
}
