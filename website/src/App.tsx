import React from "react";
import "./App.css";
import {
	Accordion,
	AccordionItem,
	AccordionItemHeading,
	AccordionItemButton,
	AccordionItemPanel
} from "react-accessible-accordion";
import "react-accessible-accordion/dist/fancy-example.css";

class App extends React.Component<
	{},
	{
		tube: {
			[key: string]: {
				affected_stations: string[];
				details: string | null;
				line: string;
				status: string;
			};
		};
	}
> {
	interval: any;
	constructor(props: {}) {
		super(props);
		this.state = {
			tube: {}
		};
	}
	getData() {
		return fetch("/underground")
			.then((res) => res.json())
			.then((res) => {
				console.log(res);
				this.setState({ tube: res.current_status });
			});
	}
	componentDidMount() {
		this.getData();
		this.interval = setInterval(() => {
			this.getData();
		}, 5 * 60 * 1000);
	}
	componentWillUnmount() {
		clearInterval(this.interval);
	}
	render() {
		return (
			<div className="App">
				<h2>
					Status for the TfL network (London Undergound, Overgound, Trams and DLR)
				</h2>
				<hr />
				<Accordion
					style={{
						backgroundColor: "#12121211",
						padding: "0",
						textAlign: "left",
						fontFamily: ""
					}}
					allowZeroExpanded
				>
					{Object.keys(this.state.tube).map((k, i) => {
						let data = this.state.tube[k];
						return (
							<AccordionItem
								key={i.toString()}
								style={{
									backgroundColor: "#35353566"
								}}
							>
								<AccordionItemHeading
									style={{
										paddingBottom: "10px"
									}}
								>
									<AccordionItemButton
										style={{
											backgroundColor: "inherit",
											color: "#fff",
											cursor: "pointer",
											height: "15px",
											fontSize: "15px",
											padding: "10px 10px 10px 10px"
											/*width: 100%;
											text-align: left;
											border: none;*/
										}}
									>
										{data.line +
											(["DLR", "Trams", "Overground"].includes(data.line)
												? data.line == "Trams"
													? ""
													: " Services"
												: " Line")}{" "}
										- {data.status}{" "}
									</AccordionItemButton>
								</AccordionItemHeading>
								<AccordionItemPanel
									style={{
										fontSize: "20px"
									}}
								>
									<p>{data.details || "Regular Service"}</p>
								</AccordionItemPanel>
							</AccordionItem>
						);
					})}
				</Accordion>
				<hr />
				<a href="https://github.com/cxllm/">API Usage</a>
			</div>
		);
	}
}

export default App;
