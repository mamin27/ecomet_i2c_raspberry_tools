program emc2301;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, emc2301_display, emc2301_read, emc2301_graph, universal
  { you can add units after this };

{$R *.res}

begin
  RequireDerivedFormResource:=True;
  Application.Scaled:=True;
  Application.Initialize;
  Application.CreateForm(TForm_emc2301, Form_emc2301);
  Application.CreateForm(TForm_graph, Form_graph);
  Application.Run;
end.

