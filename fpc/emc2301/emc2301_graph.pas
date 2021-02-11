unit emc2301_graph;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, TAGraph, TASources,
  TASeries;

type

  { TForm_graph }

  TForm_graph = class(TForm)
    Chart_emc2301_RPM: TChart;
    RPM: TLineSeries;
    UserDefinedChartSource_RPM: TUserDefinedChartSource;
  private

  public

  end;

var
  Form_graph: TForm_graph;

implementation

{$R *.lfm}

end.

