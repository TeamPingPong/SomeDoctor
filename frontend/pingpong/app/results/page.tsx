'use client'

import { useState, useMemo, useEffect } from 'react'
import { Radar, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useResultStore } from '@/store/resultStore'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
)

interface RadarData {
  [key: string]: number;
}

interface Participant {
  name: string;
  score: number;
  radarData: RadarData;
  reasoning: string;
}

interface AnalysisData {
  participants: Participant[];
  finalScore: number;
  finalScoreDescription: string;
  categoryDescriptions: {
    [key: string]: string;
  };
  advice: string;
}

interface ColorMap {
  [key: string]: string;
}

export default function Results() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const result = useResultStore((state) => state.result)
  const [participantColors, setParticipantColors] = useState<ColorMap>({})

  // result가 없을 때도 useMemo는 정상적으로 호출되어야 함
  const analysisData: AnalysisData | null = result || null
  const radarLabels = analysisData
    ? Object.keys(analysisData.participants[0].radarData)
    : []

  const chartData = useMemo(() => {
    if (!analysisData) return { labels: [], datasets: [] } // analysisData가 없을 때 빈 데이터 반환

    return {
      labels: radarLabels,
      datasets: analysisData.participants.map((participant) => {
        const color = participantColors[participant.name] || 'rgb(0, 0, 0)';
        return {
          label: participant.name,
          data: radarLabels.map(label => participant.radarData[label]),
          backgroundColor: color,
          borderColor: color,
          borderWidth: 1,
        }
      })
    }
  }, [analysisData, radarLabels, participantColors])

  useEffect(() => {
    if (result && result.participants) {
      const colors = result.participants.reduce((acc: ColorMap, participant: Participant) => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return {
          ...acc,
          [participant.name]: `rgb(${r}, ${g}, ${b})`
        };
      }, {} as ColorMap);
      setParticipantColors(colors);
    }
  }, [result]);

  if (!result) {
    return (
      <div className="container mx-auto mt-10">
        <Card>
          <CardContent>
            <p className="text-center">데이터를 불러오는 중입니다...</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!analysisData || !analysisData.participants || analysisData.participants.length === 0) {
    return (
      <div className="container mx-auto mt-10">
        <Card>
          <CardContent>
            <p className="text-center">분석 데이터가 올바르지 않습니다.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category)
  }

  return (
    <div className="container mx-auto mt-10 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-center">채팅 분석 결과</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap justify-around items-center">
            {analysisData.participants.map((participant, index) => (
              <div key={index} className="text-center p-4">
                <p className="text-2xl font-bold">{participant.score}</p>
                <p>{participant.name}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <p className="text-xl font-bold mb-2">대화 유형: {analysisData.finalScore}</p>
          <p>{analysisData.finalScoreDescription}</p>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card>
          <CardContent>
            <Radar 
              data={chartData} 
              options={{
                onClick: (event, elements) => {
                  if (elements.length > 0) {
                    const index = elements[0].index
                    handleCategoryClick(radarLabels[index])
                  }
                },
                plugins: {
                  tooltip: {
                    callbacks: {
                      label: (context) => {
                        return `${context.dataset.label}: ${context.formattedValue}`
                      }
                    }
                  }
                },
                scales: {
                  r: {
                    min: 0,
                    max: 100,
                    ticks: {
                      stepSize: 20
                    }
                  }
                }
              }}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{selectedCategory || '카테고리 설명'}</CardTitle>
          </CardHeader>
          <CardContent>
            {selectedCategory ? (
              <>
                <p className="mb-4">{analysisData.categoryDescriptions[selectedCategory]}</p>
                <Bar 
                  data={{
                    labels: chartData.datasets.map(dataset => dataset.label),
                    datasets: [{
                      label: selectedCategory,
                      data: chartData.datasets.map(dataset => 
                        dataset.data[radarLabels.indexOf(selectedCategory)]
                      ),
                      backgroundColor: chartData.datasets.map(dataset => dataset.backgroundColor),
                      borderColor: chartData.datasets.map(dataset => dataset.borderColor),
                      borderWidth: 1,
                    }]
                  }}
                  options={{
                    responsive: true,
                    indexAxis: 'y',
                    scales: {
                      x: {
                        beginAtZero: true,
                        max: 100
                      }
                    }
                  }}
                />
              </>
            ) : (
              <p>차트에서 카테고리를 선택하세요.</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>참가자별 상세 분석</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {analysisData.participants.map((participant, index) => (
              <div key={index} className="border-b pb-4 last:border-b-0">
                <h3 className="text-lg font-semibold mb-2">{participant.name}</h3>
                <p>{participant.reasoning}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>전체적인 대화에 대한 조언</CardTitle>
        </CardHeader>
        <CardContent>
          <p>{analysisData.advice}</p>
        </CardContent>
      </Card>
    </div>
  )
}