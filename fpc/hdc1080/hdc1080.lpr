program hdc1080;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, hdc1080_display, proc_py, ecomet_regex, creator, help;

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Scaled:=True;
  Application.Initialize;
  Application.CreateForm(TForm_hdc1080, Form_hdc1080);
  Application.CreateForm(TForm_creator, Form_creator);
  Application.CreateForm(TForm_help, Form_help);
  Application.Run;
end.

