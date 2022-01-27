program pca_9632;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Classes, SysUtils, CustApp, Interfaces,
  Forms, pca_display, pca_pyth_util,
  pca_read, creator, help, missing_chip;

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Title:='PCA9632 I2C Tool';
  Application.Scaled:=True;
  Application.Initialize;
  Application.ShowMainForm := False;
  Application.CreateForm(Tpca9632_main, pca9632_main);
  Application.Run;
end.
